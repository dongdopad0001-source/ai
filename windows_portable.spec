# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller recipe for the self-contained Windows distribution."""
from pathlib import Path
from PyInstaller.utils.hooks import collect_all

ROOT = Path(SPECPATH)
datas = [(str(ROOT / "main.py"), ".")]
binaries, hiddenimports = [], []
for package in (
    "streamlit", "playwright", "langchain", "langchain_community",
    "langchain_core", "langchain_experimental", "langchain_openai",
    "langchain_chroma", "langgraph", "chromadb", "faiss",
):
    package_datas, package_binaries, package_hiddenimports = collect_all(package)
    datas += package_datas
    binaries += package_binaries
    hiddenimports += package_hiddenimports

browser_dir = ROOT / "playwright-browsers"
if not browser_dir.is_dir():
    raise SystemExit("Missing playwright-browsers; run playwright install chromium first.")
datas.append((str(browser_dir), "playwright-browsers"))

a = Analysis([str(ROOT / "app.py")], pathex=[str(ROOT)], binaries=binaries,
             datas=datas, hiddenimports=hiddenimports, noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
          name="JeongSoyoonAI", console=False)
