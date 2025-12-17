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
```

---

## 🚀 How to Run
```bash
python ShutDownPC.py
```

---

## 🕹️ How It Works
- **Mode 1: Shut down at a specific time**
  - Select “Shut down at (time of day)”
  - Choose the desired time (HH:MM)
  - If the time already passed today, shutdown is scheduled for tomorrow
- **Mode 2: Shut down after a delay**
  - Select “Shut down after (HH:MM delay)”
  - Set the delay time (e.g. 01:30)
  - Countdown starts immediately

---

## 🛑 Canceling Shutdown
Once the timer is active:
- The **START** button changes to **CANCEL**
- Press **CANCEL** to immediately abort the scheduled shutdown

---

## 🧩 Project Structure

```bash
.
├── ShutDownPC.py        # Main application
├── ShutDownPC_Icon.png  # Optional app icon
└── README.md            # This file
```

--- 

## 🛠️ Technical Notes

- Uses subprocess instead of os.system for safer command execution
- OS-specific shutdown logic is isolated and easy to extend
- Written with readability and maintainability in mind

---

## 📄 License
**MIT License** — free to use, modify, and distribute.

---
## 👤 Author
Created by **Ruslan Ovcharenko**.\
If you find this project useful — ⭐ the repository!
