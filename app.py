"""Portable launcher that runs the bundled Streamlit app."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from streamlit.web import cli as stcli


def _configure_frozen_streamlit_assets(bundle_dir: Path) -> None:
    """Point Streamlit at its bundled frontend assets when frozen.

    Streamlit calculates this path from its imported module location.  In a
    PyInstaller one-file process that calculation can miss the extracted data
    directory, leaving the health endpoint available while `/` returns 404.
    """
    if not getattr(sys, "frozen", False):
        return

    static_dir = bundle_dir / "streamlit" / "static"
    if not (static_dir / "index.html").is_file():
        raise RuntimeError(f"Bundled Streamlit UI assets were not found: {static_dir}")

    from streamlit import file_util

    file_util.get_static_dir = lambda: str(static_dir)


def main() -> None:
    bundle_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    app_file = bundle_dir / "main.py"
    browser_dir = bundle_dir / "playwright-browsers"
    if not app_file.is_file():
        raise RuntimeError(f"Bundled application file was not found: {app_file}")
    if browser_dir.is_dir():
        os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(browser_dir))
    _configure_frozen_streamlit_assets(bundle_dir)
    sys.argv = [
        "streamlit", "run", str(app_file), "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
