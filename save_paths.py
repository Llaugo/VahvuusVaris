from pathlib import Path
import sys, shutil
from platformdirs import user_data_dir

APP_NAME = "VahvuusVaris"
APP_AUTHOR = "llaugo"  # any org/author string

def get_save_dir() -> Path:
    # If a folder named "game_saves" exists next to the EXE, use it (portable build).
    exe_parent = Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent
    portable_dir = exe_parent / "game_saves"
    if portable_dir.exists():
        portable_dir.mkdir(parents=True, exist_ok=True)
        return portable_dir
    # Default: per-user data dir
    d = Path(user_data_dir(APP_NAME, APP_AUTHOR)) / "game_saves"
    d.mkdir(parents=True, exist_ok=True)
    return d

def migrate_legacy_saves():
    # If you previously kept saves in repo ./game_saves during dev, copy them once.
    src = Path(__file__).resolve().parent / "game_saves"
    dst = get_save_dir()
    if src.exists():
        for p in src.iterdir():
            if p.is_file():
                shutil.copy2(p, dst / p.name)
