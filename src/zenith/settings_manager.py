import json
import os

DEFAULT_SETTINGS = {
    "theme": "dracula",
    "shortcuts": {
        "save": "Ctrl+S",
        "open_folder": "Ctrl+O",
        "new_file": "Ctrl+N",
        "split_editor": "Ctrl+E",
        "close_split": "Ctrl+W",
    }
}

class SettingsManager:
    def __init__(self):
        self._dir = os.path.join(os.path.expanduser("~"), "zenith")
        self._path = os.path.join(self._dir, "settings.json")
        self._data = {}
        self.load()

    def load(self):
        if os.path.exists(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                self._data = self._merge(DEFAULT_SETTINGS, loaded)
            except Exception:
                self._data = dict(DEFAULT_SETTINGS)
        else:
            self._data = dict(DEFAULT_SETTINGS)

    def save(self):
        os.makedirs(self._dir, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key):
        return self._data.get(key)

    def set(self, key, value):
        self._data[key] = value

    def _merge(self, default, loaded):
        result = dict(default)
        for k, v in loaded.items():
            if isinstance(v, dict) and isinstance(result.get(k), dict):
                result[k] = self._merge(result[k], v)
            else:
                result[k] = v
        return result
