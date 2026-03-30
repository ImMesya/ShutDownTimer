from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

from PyInstaller.__main__ import run as pyinstaller_run


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app_meta import APP_NAME, APP_VERSION, ENTRYPOINT, ICON_FILE


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a release package with PyInstaller.")
    parser.add_argument(
        "--version",
        default=os.environ.get("APP_VERSION", APP_VERSION),
        help="Application version embedded in the output file name.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing build artifacts before packaging.",
    )
    return parser.parse_args()


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> int:
    args = parse_args()
    target_name = f"{APP_NAME}-{args.version}"
    dist_dir = PROJECT_ROOT / "dist"
    build_dir = PROJECT_ROOT / "build"

    if args.clean:
        remove_path(build_dir)
        remove_path(dist_dir / f"{target_name}.exe")
        remove_path(dist_dir / target_name)
        remove_path(dist_dir / f"{target_name}.app")

    os.environ["APP_NAME"] = APP_NAME
    os.environ["APP_VERSION"] = args.version
    os.environ["ENTRYPOINT"] = ENTRYPOINT
    os.environ["ICON_FILE"] = ICON_FILE

    pyinstaller_args = [
        "--noconfirm",
        "--clean",
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(build_dir),
        str(PROJECT_ROOT / "packaging" / "ShutdownTimer.spec"),
    ]
    pyinstaller_run(pyinstaller_args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
