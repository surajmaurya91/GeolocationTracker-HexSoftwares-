
# 📱 Phone GeoLocator — Live Phone Number Tracking App

Phone GeoLocator is a web-based tool that allows users to track the **country, carrier, timezone & map location** of any phone number worldwide.
It uses **phonenumbers library + Google Maps API** to display accurate geographical details in a clean UI.

---

## 🚀 Features

✔ Track **any international phone number**
✔ Shows **location on map with marker pin**
✔ Displays country, carrier & timezone information
✔ Map loads instantly inside page (no redirect)
✔ Includes sample phone numbers for quick testing
✔ Lightweight, fast & mobile responsive

---

## 🛠 Tech Stack

| Component        | Used                                       |
| ---------------- | ------------------------------------------ |
| Backend          | Python + Flask                             |
| API / Mapping    | Google Maps API Embed                      |
| Parsing          | phonenumbers (geocoder, carrier, timezone) |
| Frontend         | HTML + CSS + JavaScript                    |
| Deployment Ready | Yes                                        |

---

## 📂 Project Structure

```
Phone-GeoLocator/
│── app.py
│── README.md
│── requirements.txt
│
├── templates/
│     └── index.html
│
└── static/
      ├── style.css
      └── script.js
```

---

## 🔧 Installation & Setup

### 1️⃣ Install required packages

```bash
pip install flask phonenumbers
```

### 2️⃣ Run the application

```bash
python app.py
```

### 3️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 🔑 Google Maps API Setup

To display maps properly, you must use your Google Maps API key.

💡 Replace this inside script.js:

```js
const mapUrl = `https://www.google.com/maps/embed/v1/place?key=YOUR_API_KEY&q=${lat},${lng}`;
```

Example:

```js
key=AIzaSyD4osZhNQ6PfJ78JyGrlqjq5rGl_MdwnOo
```

---

## 🧪 Sample Numbers for Testing

| Country        | Example Number |
| -------------- | -------------- |
| India 🇮🇳     | +919876543210  |
| USA 🇺🇸       | +14155552671   |
| UK 🇬🇧        | +447911123456  |
| Australia 🇦🇺 | +61491570156   |

---

## 🏆 Future Improvements

🔹 Live GPS tracking
🔹 Dark theme + animated UI
🔹 Track multiple numbers at once
🔹 Location accuracy boost model

---

## 📜 License

This project is open source under **MIT License**.
Feel free to modify, improve & use in your projects.

---

## 👨‍💻 Developer

Built by **Suraj Maurya**
🚀 Passionate Python & AI Developer
🔗 Future-ready tech builder

---

If you want, I can also generate:

📄 Project PDF
🖼 UI preview screenshots
🌐 Deployment guide for Render / Railway / Vercel

Just ask 😎
