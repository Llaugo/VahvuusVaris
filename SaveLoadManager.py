# save_system.py
from pathlib import Path
import os, sys, pickle, tempfile

def default_save_dir(app_name="VahvuusVaris") -> Path:
    if sys.platform == "win32":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:  # Linux / other (XDG)
        base = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / app_name

class SaveLoadSystem:
    def __init__(self, file_extension=".save", save_folder=None, app_name="VahvuusVaris"):
        ext = file_extension if file_extension.startswith(".") else "." + file_extension
        self.file_extension = ext
        self.save_folder = Path(save_folder) if save_folder else default_save_dir(app_name)
        self.save_folder.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        # sanitize for Windows
        safe = "".join(c for c in name if c not in r'\/:*?"<>|')
        return self.save_folder / f"{safe}{self.file_extension}"

    def save_data(self, data, name: str) -> None:
        target = self._path(name)
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile("wb", delete=False, dir=self.save_folder) as tmp:
                tmp_path = Path(tmp.name)
                pickle.dump(data, tmp, protocol=pickle.HIGHEST_PROTOCOL)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(tmp_path, target)  # atomic
        finally:
            if tmp_path and tmp_path.exists():
                try: tmp_path.unlink()
                except FileNotFoundError: pass

    def load_data(self, name: str, default=None):
        p = self._path(name)
        try:
            with open(p, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return default

    def check_for_file(self, name: str) -> bool:
        return self._path(name).exists()

    def load_game_data(self, files_to_load, default_data):
        out = [self.load_data(n, default_data[i]) for i, n in enumerate(files_to_load)]
        return tuple(out) if len(out) > 1 else out[0]

    def save_game_data(self, data_to_save, file_names):
        for data, name in zip(data_to_save, file_names):
            self.save_data(data, name)

    def remove_files(self, file_names):
        for name in file_names:
            p = self._path(name)
            if p.exists():
                p.unlink()
