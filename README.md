# Skypot: A Honeypot Attack Analysis Dashboard

Skypot is a cybersecurity project that integrates a Cowrie SSH honeypot with a Django-based dashboard for real-time attack monitoring and analysis. 
This dashboard provides valuable insights into malicious SSH login attempts, visualizing attacker trends using Folium (heatmaps), Plotly (charts), and tables.

---

## 🚀 Features

- **📍 Attack Map**: Visualize attack sources on an interactive heatmap with Folium.
- **📊 Data Insights**: Track attack trends, top attackers, and most-used credentials.
- **📌 Log Rotation **: Automates log management and parsing for optimal performance.
- **🔧 Dockerized Deployment**: Easily deploy the dashboard in a containerized environment.
- **🌐 Nginx Reverse Proxy**: Securely serve the application with HTTPS support.

---

## 📷 Dashboard Overview

Access the Live Dashboard at:
`https://dash.skky.tech`


---

## 🛠️ Installation & Setup

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/Skky-dev/SkyPot.git
cd SkyPot
```

### **2️⃣ Build and Run with Docker**
```sh
docker-compose up --build -d
```


## 📌 Log Rotation

- Logs from the Cowrie honeypot are periodically parsed to extract attack details.

- Visualization files (maps and charts) are generated and updated dynamically


---

## 🏗️ Tech Stack

- **Backend**: Django, SQLite/PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Visualizations**: Plotly, Folium
- **Deployment**: Docker, Nginx

---

## 📞 Contact
For any inquiries, feel free to reach out via GitHub Issues.

---

> 🚀 _Happy Hacking! Stay Secure!_

