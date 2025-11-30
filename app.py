import os
import tempfile
import uuid
from flask import Flask, render_template, request, jsonify, send_file
import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import folium

app = Flask(__name__)

# Try to read API key from environment first (recommended).
# If not set, fallback to the key the user provided (only for quick testing).
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyD4osZhNQ6PfJ78JyGrlqjq5rGl_MdwnOo")

# Basic fallback lat/lon for a few countries (used only if Google fails)
FALLBACK_COORDS = {
    "IN": (20.5937, 78.9629),   # India
    "US": (37.0902, -95.7129),  # United States (center)
    "GB": (55.3781, -3.4360),   # United Kingdom
    "AU": (-25.2744, 133.7751), # Australia
    "JP": (36.2048, 138.2529),  # Japan
    "DE": (51.1657, 10.4515),   # Germany
    # add more if you want
}


def geocode_place(place_query: str):
    """Return (lat, lng) from Google Geocoding API for a given text query.
       Returns (None, None) on failure.
    """
    if not GOOGLE_API_KEY:
        return None, None

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": place_query, "key": GOOGLE_API_KEY}
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        if data.get("status") == "OK" and data.get("results"):
            loc = data["results"][0]["geometry"]["location"]
            return loc.get("lat"), loc.get("lng")
    except Exception as e:
        app.logger.debug("Geocoding error: %s", e)
    return None, None


def create_map_file(lat: float, lng: float, popup_text: str):
    """Create a folium map and save to a unique temp html file. Return filename (basename)."""
    m = folium.Map(location=[lat, lng], zoom_start=5)
    folium.Marker([lat, lng], popup=popup_text, tooltip=popup_text).add_to(m)

    unique_name = f"map_{uuid.uuid4().hex}.html"
    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, unique_name)
    m.save(path)
    return unique_name


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/track", methods=["POST"])
def track():
    # This endpoint returns JSON (UI will update dynamically)
    phone_input = (request.form.get("phone") or "").strip()
    if not phone_input:
        return jsonify({"error": "Please enter a phone number (with or without +)."}), 400

    # Ensure plus sign for parsing (phonenumbers accepts both forms but we'll normalize)
    if not phone_input.startswith("+"):
        phone_input = "+" + phone_input

    try:
        num = phonenumbers.parse(phone_input, None)
    except Exception as e:
        return jsonify({"error": "Invalid phone number format. Use +CountryCodeNumber"}), 400

    is_valid = phonenumbers.is_valid_number(num)
    region_code = phonenumbers.region_code_for_number(num)  # e.g., "IN", "US"
    country_name = geocoder.description_for_number(num, "en") or region_code or "Unknown"
    sim_name = carrier.name_for_number(num, "en") or "Unknown"
    tz = None
    try:
        tz = phonenumbers.timezone.time_zones_for_number(num)
    except Exception:
        tz = []

    # Try geocoding: prefer precise geocoder result; send "Country Country" query (helps for some countries)
    query_candidates = []
    if country_name and country_name != region_code:
        query_candidates.append(f"{country_name} country")
        query_candidates.append(country_name)
    if region_code:
        query_candidates.append(f"{region_code} country")
        query_candidates.append(region_code)

    lat = lon = None
    for q in query_candidates:
        lat, lon = geocode_place(q)
        if lat is not None and lon is not None:
            break

    # Fallback to predefined coords if Google fails
    if lat is None or lon is None:
        fallback = FALLBACK_COORDS.get(region_code)
        if fallback:
            lat, lon = fallback
        else:
            # final fallback to world center
            lat, lon = (0.0, 0.0)

    # Create a map file and return its path (URL to fetch)
    popup = f"{phone_input} — {country_name}"
    filename = create_map_file(lat, lon, popup)
    map_url = f"/view_map/{filename}"

    response = {
        "number": phone_input,
        "is_valid": is_valid,
        "country": country_name,
        "region_code": region_code,
        "carrier": sim_name,
        "timezone": tz,
        "map_url": map_url,
        "map_file": filename
    }
    return jsonify(response)


@app.route("/view_map/<filename>")
def view_map(filename):
    # Serve the temporary map file if it exists
    temp_dir = tempfile.gettempdir()
    path = os.path.join(temp_dir, filename)
    if not os.path.exists(path):
        return "Map not found or expired.", 404
    return send_file(path)


if __name__ == "__main__":
    # Use host=0.0.0.0 only if you want other devices to reach it on the network.
    app.run(debug=True, port=5000)
