# Shutdown Timer (PyQt5)

A simple cross-platform desktop application that allows you to schedule a system shutdown **at a specific time** or **after a delay**.  
Built with **Python + PyQt5**, focused on clarity, safety, and clean UI.

---

## ✨ Features

- 🕒 **Two shutdown modes**
  - **Shut down at** a specific time of day (today or tomorrow)
  - **Shut down after** a delay (HH:MM)
- 🔄 **Start / Cancel** toggle button
- ⚠️ **Safety confirmation** for short delays (under 5 minutes)
- 💻 **Cross-platform support**
  - Windows
  - Linux
  - macOS
- 🧼 Clean, refactored, and well-commented code
- 🧠 Automatic handling if the selected time has already passed (schedules for the next day)

---

## 🖥️ Supported Operating Systems

| OS       | Status | Notes |
|---------|--------|------|
| Windows | ✅ Full | Uses native `shutdown /s /t` |
| Linux   | ✅ Full | May require `sudo` permissions |
| macOS   | ✅ Full | Uses system `shutdown` command |

> ⚠️ On **Linux/macOS**, you may need to run the app with administrator privileges to allow shutdown scheduling.

---

## 📦 Requirements

- Python **3.9+**
- PyQt5

Install dependencies:
```bash
pip install PyQt5
