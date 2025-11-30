const form = document.getElementById("trackForm");
const status = document.getElementById("status");
const info = document.getElementById("info");
const mapWrap = document.getElementById("mapWrap");

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  status.textContent = "Searching…";
  info.classList.add("hidden");
  mapWrap.classList.add("hidden");

  const formData = new FormData(form);
  try {
    const resp = await fetch("/track", { method: "POST", body: formData });
    const data = await resp.json();

    if (!resp.ok) {
      status.textContent = data.error || "Error occurred";
      return;
    }

    // Fill info
    document.getElementById("res_number").textContent = data.number;
    document.getElementById("res_country").textContent = data.country;
    document.getElementById("res_region").textContent = data.region_code;
    document.getElementById("res_carrier").textContent = data.carrier;
    document.getElementById("res_tz").textContent = (data.timezone || []).join(", ");

    status.textContent = data.is_valid ? "Valid number" : "Parsed (may not be a valid number)";
    info.classList.remove("hidden");

    // Load map in iframe
    const mapFrame = document.getElementById("mapFrame");
    mapFrame.src = data.map_url + "?cache=" + Date.now();
    mapWrap.classList.remove("hidden");

  } catch (err) {
    status.textContent = "Network or server error";
    console.error(err);
  }
});

function fill(v){
  document.getElementById("phoneInput").value = v;
}
