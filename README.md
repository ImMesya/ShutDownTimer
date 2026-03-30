# Shutdown Timer

Shutdown Timer is a small cross-platform desktop application for scheduling a system shutdown either at a specific time of day or after a fixed delay.

The project is built with Python and PyQt5 and is designed to stay simple: one window, two scheduling modes, and predictable behavior across Windows, Linux, and macOS.

## Overview

- Schedule shutdown for a specific time today or, if that time has already passed, tomorrow.
- Schedule shutdown after a delay in `HH:MM` format.
- Cancel an active shutdown timer from the same window.
- Confirm short delays before applying them.
- Build single-file release artifacts for Windows and Linux.
- Publish Windows, Linux, and macOS releases automatically through GitHub Actions.

## Supported Platforms

| Platform | Status | Implementation |
| --- | --- | --- |
| Windows | Supported | Uses `shutdown /s /t <seconds>` and `shutdown /a` |
| Linux | Supported | Uses `shutdown -h +<minutes>` and `shutdown -c` |
| macOS | Supported | Uses `shutdown -h +<minutes>` and `shutdown -c` |

Linux and macOS may require elevated privileges to schedule a shutdown, depending on the system configuration.

## Requirements

- Python 3.9 or newer
- PyQt5

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running From Source

```bash
python ShutDownPC.py
```

## Usage

1. Choose one of the two modes:
   - `Shut down at`: schedule shutdown for a specific time of day.
   - `Shut down after`: schedule shutdown after a delay in `HH:MM`.
2. Set the desired time or delay.
3. Click `START` to schedule the shutdown.
4. Click `CANCEL` to abort an active timer.

If the selected time has already passed for the current day, the application automatically schedules the shutdown for the next day.

For delays shorter than five minutes, the application shows an additional confirmation dialog.

## Building

### Local Windows Build

The repository includes a local Windows build script:

```bat
build_win.bat
```

This script:

- creates the local virtual environment if needed
- installs or updates build dependencies
- reads the version from `app_meta.py`
- produces a one-file Windows executable in `dist/`

You can also run the build entry point directly:

```bash
python packaging/build_release.py --clean --version 1.0.5
```

### Release Packaging

- Windows and Linux releases are built as trimmed `PyInstaller --onefile` packages.
- macOS releases are built as an application bundle and published as a zip archive.
- The release build profile removes unused Qt components to reduce package size and improve startup time compared with a generic one-file build.

## Automated GitHub Releases

The repository contains a GitHub Actions workflow that builds and publishes release artifacts for:

- Windows
- Linux
- macOS

Release process:

1. Update the version in `app_meta.py`.
2. Commit and push the changes.
3. Create a matching tag such as `v1.0.5`.
4. Push the tag.

When the tag is pushed, GitHub Actions:

- validates that the tag matches the version declared in `app_meta.py`
- builds platform-specific release artifacts
- creates or updates the GitHub Release
- uploads the generated zip files as release assets

## Project Structure

```text
.
|-- ShutDownPC.py              # main application window and shutdown logic
|-- app_meta.py                # application metadata and version
|-- packaging/
|   |-- build_release.py       # local release build entry point
|   `-- ShutdownTimer.spec     # optimized PyInstaller configuration
`-- .github/workflows/
    `-- build.yml              # automated multi-platform release pipeline
```

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Created by Ruslan Ovcharenko.
