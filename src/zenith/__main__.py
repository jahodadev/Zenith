"""Vstupní bod aplikace Zenith Code Editor."""

from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from .editor import Editor
from .sidebar import Sidebar
from .settings_manager import SettingsManager
from .settings_dialog import SettingsDialog
from .themes import THEMES


class EditorArea(QWidget):
    """Kontejner spravující více instancí editoru v rozděleném zobrazení."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet(
            "QSplitter::handle { background-color: #191a21; }"
        )
        layout.addWidget(self.splitter)

        self.editors: list[Editor] = []
        self._currentShortcuts: dict[str, str] | None = None
        self._currentTheme: dict[str, str] | None = None
        self.addEditor()

    def addEditor(self) -> Editor:
        """Přidá nový panel editoru a rovnoměrně rozdělí dostupný prostor."""
        editor = Editor()
        self.editors.append(editor)
        self.splitter.addWidget(editor)
        if self._currentShortcuts:
            editor.applyShortcuts(self._currentShortcuts)
        if self._currentTheme:
            editor.applyTheme(self._currentTheme)
        count = len(self.editors)
        self.splitter.setSizes([1000 // count] * count)
        return editor

    def closeActiveEditor(self) -> None:
        """Zavře aktivní editor. Pokud je otevřený jen jeden, nic neprovede."""
        if len(self.editors) <= 1:
            return
        editor = self._getActiveEditor()
        if editor:
            self.editors.remove(editor)
            editor.deleteLater()

    def openFile(self, filePath: str) -> None:
        editor = self._getActiveEditor()
        if editor:
            editor.openFile(filePath)

    def saveFile(self) -> None:
        editor = self._getActiveEditor()
        if editor:
            editor.saveFile()

    def applyShortcuts(self, shortcuts: dict[str, str]) -> None:
        """Uloží zkratky a předá je všem otevřeným editorům."""
        self._currentShortcuts = shortcuts
        for editor in self.editors:
            editor.applyShortcuts(shortcuts)

    def applyTheme(self, theme: dict[str, str]) -> None:
        """Aplikuje téma na oddělovač a všechny otevřené editory."""
        self._currentTheme = theme
        self.splitter.setStyleSheet(
            f"QSplitter::handle {{ background-color: {theme['border']}; }}"
        )
        for editor in self.editors:
            editor.applyTheme(theme)

    def _getActiveEditor(self) -> Editor | None:
        """Vrátí editor s fokusem, nebo první v seznamu. Pokud žádný není, vrátí None."""
        for editor in self.editors:
            if editor.textEdit.hasFocus():
                return editor
        if self.editors:
            return self.editors[0]
        return None


class MainWindow(QMainWindow):
    """Hlavní okno aplikace spojující postranní panel a oblast editorů."""

    def __init__(self):
        super().__init__()

        self.settings = SettingsManager()

        self.setWindowTitle("Zenith - Code Editor")
        self.resize(1000, 700)

        self.splitter = QSplitter(Qt.Horizontal)

        self.sidebar = Sidebar()
        self.editorArea = EditorArea()

        self.sidebar.fileDoubleClicked.connect(self.editorArea.openFile)
        self.sidebar.saveFileClicked.connect(self.editorArea.saveFile)
        self.sidebar.settingsClicked.connect(self.openSettings)

        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.editorArea)

        self.splitter.setSizes([200, 800])
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #191a21; }")

        self.setCentralWidget(self.splitter)

        self.splitAction = QAction(self)
        self.splitAction.triggered.connect(self.editorArea.addEditor)
        self.addAction(self.splitAction)

        self.closeAction = QAction(self)
        self.closeAction.triggered.connect(self.editorArea.closeActiveEditor)
        self.addAction(self.closeAction)

        self._applySettings()

    def openSettings(self) -> None:
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            self._applySettings()

    def _applySettings(self) -> None:
        """Načte nastavení a aplikuje téma a zkratky na celé UI."""
        shortcuts = self.settings.get("shortcuts")
        self.splitAction.setShortcut(QKeySequence(shortcuts.get("split_editor", "Ctrl+E")))
        self.closeAction.setShortcut(QKeySequence(shortcuts.get("close_split", "Ctrl+W")))
        self.editorArea.applyShortcuts(shortcuts)

        themeKey = self.settings.get("theme")
        theme = THEMES.get(themeKey, THEMES["dracula"])
        self.editorArea.applyTheme(theme)
        self.sidebar.setStyleSheet(
            f"background-color: {theme['sidebar_bg']}; color: {theme['foreground']};"
        )
        self.sidebar.folderLabel.setStyleSheet(
            f"color: {theme['comment']}; font-size: 11px; font-weight: bold;"
            f" padding: 10px 10px 5px 10px; margin: 0px;"
            f" background-color: {theme['sidebar_bg']}; border: none;"
        )
        self.sidebar.tree.setStyleSheet(
            f"QTreeView {{ background-color: {theme['sidebar_bg']}; color: {theme['foreground']}; border: none; }}"
        )
        self.sidebar.toolbar.setStyleSheet(
            f"background-color: {theme['toolbar_bg']}; border-bottom: 1px solid {theme['border']};"
        )
        self.splitter.setStyleSheet(
            f"QSplitter::handle {{ background-color: {theme['border']}; }}"
        )


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
