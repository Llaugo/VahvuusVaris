from pathlib import Path
import sys

def _base_path() -> Path:
    # onefile: PyInstaller extracts to a temp dir at _MEIPASS
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    # running from source
    return Path(__file__).resolve().parent

def resource_path(*parts) -> str:
    return str(_base_path().joinpath(*parts))
