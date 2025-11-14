# Airport Tracker — Live Flight Dashboard

A real-time flight tracking application with live OpenSky Network data, weather forecasts, and professional visualizations. Includes both a terminal-based menu app and a modern web UI with interactive Plotly charts.

## 🚀 Quick Start (One Command!)

### Easiest: One-Click Launcher

```powershell
cd "C:\Users\basmussen\Desktop\Flight Trackers\New folder"
.\start.ps1
```

✅ This does everything:
- ✓ Checks Python 3.10+
- ✓ Installs dependencies (one-time)
- ✓ Downloads brand logo
- ✓ Starts production server on http://127.0.0.1:5001
- ✓ Opens the web UI automatically in your browser
- Press **Ctrl+C** to stop

---

### Alternative: Traditional Method

```powershell
cd "C:\Users\basmussen\Desktop\Flight Trackers\New folder"
.\run_server.ps1
```

Or if scripts are blocked:
```powershell
powershell -ExecutionPolicy Bypass -File .\start.ps1
```

---

## 📊 What You'll See

### Web UI Dashboard (http://127.0.0.1:5001)
- **Interactive Plotly Charts**:
  - Flight Status (pie chart)
  - Hourly Activity (line chart)
  - Airline On-Time Performance (bar chart)
  - Live Aircraft Map (scattergeo plot with lat/lon)
- **Matplotlib Plots** (sidebar buttons):
  - Comprehensive 6-panel dashboard
  - Individual visualizations (runway, delays, weather, etc.)
- **Live JSON Data**:
  - Real flights and weather (first 50 flights shown)
  - Updates every 15 seconds

---

## 🛠 Installation & Dependencies

If `run_server.ps1` fails, install manually:

```powershell
python -m pip install -r requirements.txt
```

**Required packages**:
- Flask>=2.0 (REST API)
- Plotly (interactive charts)
- Pandas, NumPy (data handling)
- Matplotlib, Seaborn (professional plots)
- Requests (HTTP calls)
- Redis>=4.0 (optional, for advanced caching)

---

## Alternative: Terminal-Based App

For the classic terminal menu interface:

```powershell
python "Airport Tracker.py"
```

Interactive menu with:
- Arrivals & departures boards
- Flight status and delays
- Weather comparison
- 7 professional matplotlib plots

---

## 🌐 Alternative: Dash Web App

For the original Dash-based UI:

```powershell
python app.py
```

Then visit http://127.0.0.1:8050

---

## ⚙️ Advanced: Custom Port / Manual Launch

```powershell
python api.py --host 127.0.0.1 --port 5002 --open
```

Or without auto-opening:
```powershell
python api.py --host 127.0.0.1 --port 5001
```

Then visit http://127.0.0.1:5001 manually.

---

## 🖱 Create a Desktop Shortcut (Windows)

If you'd like to start the server with a double-click, create a desktop shortcut that runs the included PowerShell launcher:

Open PowerShell and run (from the project folder):

```powershell
.\\create_shortcut.ps1
```

This will create a `Airport Tracker.lnk` on your desktop that runs `run_server.ps1` (which installs requirements and launches the API). If you prefer, you can run `run_server.ps1` directly:

```powershell
.\\run_server.ps1
```

If PowerShell blocks running scripts, run with:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_server.ps1
```

---

## 🛌 Run the server in background / auto-start at logon

You can run the server in the background (hidden window) or install a scheduled task so the app starts automatically when you log in.

- Start in background now (one-shot):

```powershell
cd "C:\Users\basmussen\Desktop\Flight Trackers\New folder"
.\start_background.ps1
```

- Install scheduled task to auto-run at logon:

```powershell
cd "C:\Users\basmussen\Desktop\Flight Trackers\New folder"
.\install_schtask.ps1
```

This creates a Windows Scheduled Task named `AirportTracker` (default) that will run `run_server.ps1` at logon for the current user. To remove it:

```powershell
cd "C:\Users\basmussen\Desktop\Flight Trackers\New folder"
.\uninstall_schtask.ps1
```

Notes:
- The scheduled task runs the PowerShell script in a hidden window; logs (if any) will appear in the project folder when the server writes output.
- If you prefer the desktop shortcut to launch the background runner, edit `create_shortcut.ps1` and set the default `TargetScript` to `start_background.ps1`.

Log rotation and production server
- The background runner rotates logs automatically and keeps the last 5 log files: `server.log.1` .. `server.log.5` and `server.err.1` .. `server.err.5`.
- The server is now served with Waitress (a production-ready WSGI server for Windows) instead of Flask's development server. The project includes `serve_prod.py` which launches Waitress.

If you want to run the production server directly (no background starter):

```powershell
python serve_prod.py --host 127.0.0.1 --port 5001
```


## 📡 Data Sources

- **Flights**: [OpenSky Network API](https://opensky-network.org/api/) — Free real-time ADS-B data (no auth required)
- **Weather**: [Open-Meteo API](https://open-meteo.com/) — Free weather (no auth required)
- **Coverage**: Wichita area (ICT) + extended US weather data

---

## 🔍 Troubleshooting

**"Connection refused" error?**
- Check Windows Firewall allows port 5001 (script tries to auto-add rule)
- Try a different port: `python api.py --port 5002 --open`
- Ensure Flask isn't already running on that port

**"ModuleNotFoundError"?**
- Install dependencies: `python -m pip install -r requirements.txt`

**No live data showing?**
- External APIs (OpenSky, Open-Meteo) might be rate-limited or down
- UI will retry every 15 seconds automatically
- Check browser console (F12) for network errors

---

## 📁 Project Structure

```
Flight Trackers/
├── Aiport Tracker.py          # Main tracker class + matplotlib charts
├── api.py                     # Flask REST API + static UI server
├── app.py                     # Alternative Dash web app
├── requirements.txt           # Python dependencies
├── run_server.ps1             # Launch script (install + run + firewall)
├── create_shortcut.ps1        # Create desktop shortcut
├── static/
│   ├── index.html             # Web UI
│   ├── app.js                 # Plotly charts + refresh logic
│   └── styles.css             # Responsive styling
└── README.md                  # This file
```

---

**Enjoy your Airport Tracker! 🛫**

