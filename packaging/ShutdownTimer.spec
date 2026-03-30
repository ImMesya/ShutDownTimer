# -*- mode: python ; coding: utf-8 -*-

from __future__ import annotations

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(SPECPATH).resolve().parent
APP_NAME = os.environ.get("APP_NAME", "ShutdownTimer")
APP_VERSION = os.environ.get("APP_VERSION", "1.0.5")
ENTRYPOINT = PROJECT_ROOT / os.environ.get("ENTRYPOINT", "ShutDownPC.py")
ICON_PATH = PROJECT_ROOT / os.environ.get("ICON_FILE", "icon.ico")
TARGET_NAME = f"{APP_NAME}-{APP_VERSION}"

EXCLUDED_MODULES = [
    "PyQt5.QtBluetooth",
    "PyQt5.QtDesigner",
    "PyQt5.QtHelp",
    "PyQt5.QtLocation",
    "PyQt5.QtMultimedia",
    "PyQt5.QtMultimediaWidgets",
    "PyQt5.QtNetwork",
    "PyQt5.QtNfc",
    "PyQt5.QtOpenGL",
    "PyQt5.QtPositioning",
    "PyQt5.QtPrintSupport",
    "PyQt5.QtQml",
    "PyQt5.QtQuick",
    "PyQt5.QtSensors",
    "PyQt5.QtSerialPort",
    "PyQt5.QtSql",
    "PyQt5.QtSvg",
    "PyQt5.QtTest",
    "PyQt5.QtWebChannel",
    "PyQt5.QtWebEngineCore",
    "PyQt5.QtWebEngineWidgets",
    "PyQt5.QtWebSockets",
    "PyQt5.QtWinExtras",
    "PyQt5.QtXml",
    "matplotlib",
    "numpy",
    "pandas",
    "PIL",
    "scipy",
    "tk",
    "tcl",
    "tkinter",
]

ALLOWED_QT_PLUGIN_SUFFIXES = {
    "win32": (
        "PyQt5/Qt5/plugins/platforms/qwindows.dll",
        "PyQt5/Qt5/plugins/imageformats/qico.dll",
        "PyQt5/Qt5/plugins/styles/qwindowsvistastyle.dll",
    ),
    "linux": (
        "PyQt5/Qt5/plugins/platforms/libqxcb.so",
        "PyQt5/Qt5/plugins/imageformats/libqico.so",
    ),
    "darwin": (
        "PyQt5/Qt5/plugins/platforms/libqcocoa.dylib",
        "PyQt5/Qt5/plugins/imageformats/libqico.dylib",
    ),
}

UNUSED_QT_BINARIES = (
    "PyQt5/Qt5/bin/d3dcompiler_47.dll",
    "PyQt5/Qt5/bin/libEGL.dll",
    "PyQt5/Qt5/bin/libGLESv2.dll",
    "PyQt5/Qt5/bin/opengl32sw.dll",
)


def keep_qt_runtime(entry: tuple[str, str, str]) -> bool:
    dest = entry[0].replace("\\", "/")
    lowered = dest.lower()

    if lowered.endswith(tuple(path.lower() for path in UNUSED_QT_BINARIES)):
        return False

    if "pyqt5/qt5/plugins/" not in lowered:
        return True

    allowed = ALLOWED_QT_PLUGIN_SUFFIXES.get(sys.platform, ())
    return lowered.endswith(tuple(path.lower() for path in allowed))


datas = [(str(ICON_PATH), ".")] if ICON_PATH.exists() else []

a = Analysis(
    [str(ENTRYPOINT)],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=EXCLUDED_MODULES,
    noarchive=False,
    optimize=2,
)

a.datas = [entry for entry in a.datas if keep_qt_runtime(entry)]
a.binaries = [entry for entry in a.binaries if keep_qt_runtime(entry)]

pyz = PYZ(a.pure, a.zipped_data)

runtime_tmpdir = None
if sys.platform.startswith("win"):
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        runtime_tmpdir = str(Path(local_app_data) / APP_NAME / "runtime")

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=TARGET_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    runtime_tmpdir=runtime_tmpdir,
    icon=str(ICON_PATH) if ICON_PATH.exists() else None,
)
