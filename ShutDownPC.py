# -*- coding: utf-8 -*-
"""
Shutdown Timer (PyQt5)

Features:
- Two modes:
  1) Shutdown AT a specific time of day (today or tomorrow).
  2) Shutdown AFTER a delay (HH:MM).
- Start / Cancel toggle button.
- Safety confirmation if delay is < 5 minutes.
- Cross-platform command handling:
  - Windows: shutdown /s /t <seconds>, cancel: shutdown /a
  - Linux/macOS: uses 'shutdown -h +<minutes>', cancel: 'shutdown -c'
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
    qApp,
)

from app_meta import APP_DISPLAY_NAME, APP_VERSION, ICON_FILE


SECONDS_IN_DAY = 24 * 60 * 60
MIN_CONFIRM_SECONDS = 5 * 60
FONT_PIXEL_SIZE = 32
START_LABEL = "START"
CANCEL_LABEL = "CANCEL"
IS_WINDOWS = sys.platform.startswith("win")
WINDOWS_SHUTDOWN_EXE = str(Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "shutdown.exe")

def resource_path(relative_path: str) -> str:
    """Get an absolute resource path for source and frozen builds."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str(base_path / relative_path)


@dataclass(frozen=True)
class ShutdownCommand:
    """Container for OS-specific shutdown/cancel commands."""
    shutdown_args: list[str]
    cancel_args: list[str]


def get_shutdown_command(seconds: int) -> ShutdownCommand:
    """
    Returns OS-appropriate shutdown and cancel commands.

    Notes:
    - Windows supports seconds directly.
    - Linux/macOS classic 'shutdown' generally supports minutes granularity.
    """
    if IS_WINDOWS:
        # Windows: seconds supported
        return ShutdownCommand(
            shutdown_args=[WINDOWS_SHUTDOWN_EXE, "/s", "/t", str(int(seconds))],
            cancel_args=[WINDOWS_SHUTDOWN_EXE, "/a"],
        )

    # Linux/macOS: use minutes (ceil to 1 minute if >0)
    minutes = max(1, (int(seconds) + 59) // 60)
    return ShutdownCommand(
        shutdown_args=["shutdown", "-h", f"+{minutes}"],
        cancel_args=["shutdown", "-c"],
    )


def run_command(args: list[str]) -> tuple[bool, str]:
    """
    Runs a command safely.
    Returns: (ok, message). If ok=False, message contains stderr/stdout.
    """
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False,
        )
        ok = (completed.returncode == 0)
        msg = (completed.stderr or completed.stdout or "").strip()
        return ok, msg
    except FileNotFoundError:
        return False, f"Command not found: {args[0]}"
    except Exception as e:
        return False, f"Error running command: {e}"


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.timer_active = False

        # -------- UI setup --------
        main_layout = QVBoxLayout(self)

        # Use a large but still practical font (100px is usually too big for most screens)
        font = QFont()
        font.setPixelSize(FONT_PIXEL_SIZE)

        # Mode selection
        mode_layout = QHBoxLayout()

        self.radio_at_time = QRadioButton("Shut down at (time of day)")
        self.radio_at_time.setFont(font)
        self.radio_at_time.setChecked(True)
        self.radio_at_time.clicked.connect(self.on_mode_changed)

        self.radio_after_delay = QRadioButton("Shut down after (HH:MM delay)")
        self.radio_after_delay.setFont(font)
        self.radio_after_delay.clicked.connect(self.on_mode_changed)

        mode_layout.addWidget(self.radio_at_time)
        mode_layout.addWidget(self.radio_after_delay)
        main_layout.addLayout(mode_layout)

        # Time input (same widget, interpreted differently depending on mode)
        self.time_edit = QTimeEdit()
        self.time_edit.setFont(font)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())
        main_layout.addWidget(self.time_edit)

        # Buttons
        btn_layout = QHBoxLayout()

        self.start_button = QPushButton(START_LABEL)
        self.start_button.setFont(font)
        self.start_button.clicked.connect(self.on_start_cancel_clicked)

        self.exit_button = QPushButton("EXIT")
        self.exit_button.setFont(font)
        self.exit_button.clicked.connect(self.on_exit_clicked)

        btn_layout.addWidget(self.start_button)
        btn_layout.addWidget(self.exit_button)
        main_layout.addLayout(btn_layout)

        self.setWindowTitle(APP_DISPLAY_NAME)

        # Icon is optional; don't crash if missing
        icon_path = resource_path(ICON_FILE)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    # -------- Event handlers --------

    def on_exit_clicked(self) -> None:
        qApp.quit()

    def on_start_cancel_clicked(self) -> None:
        if self.timer_active:
            self.cancel_shutdown_timer()
        else:
            self.start_shutdown_timer()

    def on_mode_changed(self) -> None:
        """
        When switching modes, reset the time_edit appropriately:
        - At-time mode: set current time.
        - After-delay mode: set 00:00 (user sets delay).
        """
        if self.radio_at_time.isChecked():
            self.time_edit.setTime(QTime.currentTime())
        else:
            self.time_edit.setTime(QTime(0, 0))

    # -------- Core logic --------

    def compute_seconds_until_shutdown(self) -> int:
        """
        Computes delay in seconds based on selected mode and input time.
        """
        now = QDateTime.currentDateTime()

        if self.radio_at_time.isChecked():
            # Interpret input as time-of-day
            target_time = self.time_edit.time()
            target_dt = QDateTime(now.date(), target_time)

            seconds = now.secsTo(target_dt)
            # If target time already passed today, schedule for tomorrow
            if seconds < 0:
                seconds += SECONDS_IN_DAY

            return int(seconds)

        # After-delay mode: interpret input as HH:MM delay
        delay = self.time_edit.time()
        seconds = delay.hour() * 3600 + delay.minute() * 60
        return int(seconds)

    def start_shutdown_timer(self) -> None:
        seconds = self.compute_seconds_until_shutdown()

        if seconds <= 0:
            QMessageBox.warning(self, "Invalid time", "Please choose a time/delay greater than 00:00.")
            return

        # Safety confirmation for very short delays
        if seconds < MIN_CONFIRM_SECONDS:
            reply = QMessageBox.question(
                self,
                "Set timer?",
                "You selected a delay under 5 minutes. Do you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        cmd = get_shutdown_command(seconds)
        ok, msg = run_command(cmd.shutdown_args)

        if not ok:
            extra = f"\n\nDetails: {msg}" if msg else ""
            QMessageBox.critical(
                self,
                "Failed to set shutdown timer",
                "Could not schedule shutdown. On Linux/macOS you may need admin permissions (sudo)."
                + extra,
            )
            return

        QMessageBox.information(
            self,
            "Timer set",
            f"Your PC will shut down in {timedelta(seconds=seconds)}.",
        )
        self.timer_active = True
        self.start_button.setText(CANCEL_LABEL)

    def cancel_shutdown_timer(self) -> None:
        # Cancel command depends on OS
        cmd = get_shutdown_command(60)  # seconds value doesn't matter for cancel_args
        ok, msg = run_command(cmd.cancel_args)

        if not ok:
            extra = f"\n\nDetails: {msg}" if msg else ""
            QMessageBox.critical(
                self,
                "Failed to cancel",
                "Could not cancel the shutdown timer."
                + extra,
            )
            return

        QMessageBox.information(self, "Cancelled", "Shutdown timer cancelled. You can set a new one.")
        self.timer_active = False
        self.start_button.setText(START_LABEL)


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_DISPLAY_NAME)
    app.setApplicationVersion(APP_VERSION)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
