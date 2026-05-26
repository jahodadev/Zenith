"""Správa nastavení editoru uložených v JSON souboru."""

from __future__ import annotations

import json
import os
from typing import Any

DEFAULT_SETTINGS: dict[str, Any] = {
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
    """Načítá a ukládá nastavení do souboru ~/.zenith/settings.json."""

    def __init__(self):
        self._dir = os.path.join(os.path.expanduser("~"), "zenith")
        self._path = os.path.join(self._dir, "settings.json")
        self._data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Načte nastavení ze souboru, při chybě použije výchozí hodnoty."""
        if os.path.exists(self._path):
            try:
                with open(self._path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                self._data = self._merge(DEFAULT_SETTINGS, loaded)
            except Exception:
                self._data = dict(DEFAULT_SETTINGS)
        else:
            self._data = dict(DEFAULT_SETTINGS)

    def save(self) -> None:
        """Uloží aktuální nastavení do souboru."""
        os.makedirs(self._dir, exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def get(self, key: str) -> Any:
        return self._data.get(key)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def _merge(self, default: dict[str, Any], loaded: dict[str, Any]) -> dict[str, Any]:
        """Rekurzivně sloučí načtená nastavení s výchozími hodnotami.

        Klíče z loaded přepíší default, vnořené slovníky se sloučí rekurzivně.
        """
        result = dict(default)
        for k, v in loaded.items():
            if isinstance(v, dict) and isinstance(result.get(k), dict):
                result[k] = self._merge(result[k], v)
            else:
                result[k] = v
        return result
