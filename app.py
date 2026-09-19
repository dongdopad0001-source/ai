"""Portable launcher that runs the bundled Streamlit app."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main() -> None:
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_file = bundle_dir / "main.py"
    browser_dir = bundle_dir / "playwright-browsers"
    if not app_file.is_file():
        raise RuntimeError(f"Bundled application file was not found: {app_file}")
    if browser_dir.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(browser_dir))
    sys.argv = [
        "streamlit", "run", str(app_file), "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
