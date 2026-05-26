"""Dialog nastavení s záložkami pro témata a klávesové zkratky."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem,
    QPushButton, QHeaderView
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from .themes import THEMES


class SettingsDialog(QDialog):
    """Modální dialog pro úpravu nastavení editoru."""

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("""
            QDialog { background-color: #21222c; color: #f8f8f2; }
            QTabWidget::pane { border: 1px solid #44475a; }
            QTabBar::tab {
                background: #1e1f29; color: #6272a4;
                padding: 8px 20px; border: none;
            }
            QTabBar::tab:selected { background: #21222c; color: #f8f8f2; }
            QPushButton {
                background-color: #44475a; color: #f8f8f2;
                border: none; border-radius: 4px; padding: 6px 16px;
            }
            QPushButton:hover { background-color: #6272a4; }
            QPushButton#saveBtn { background-color: #50fa7b; color: #1c1d26; }
            QPushButton#saveBtn:hover { background-color: #69ff94; }
            QTableWidget {
                background-color: #1e1f29; color: #f8f8f2;
                border: none; gridline-color: #44475a;
            }
            QHeaderView::section {
                background-color: #1e1f29; color: #6272a4;
                border: none; padding: 4px;
            }
            QTableWidget::item:selected { background-color: #44475a; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 16)
        layout.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._buildThemesTab(), "Themes")
        self.tabs.addTab(self._buildShortcutsTab(), "Shortcuts")
        layout.addWidget(self.tabs)

        btnLayout = QHBoxLayout()
        btnLayout.setContentsMargins(16, 8, 16, 0)
        btnLayout.addStretch()

        cancelBtn = QPushButton("Cancel")
        cancelBtn.clicked.connect(self.reject)

        saveBtn = QPushButton("Save")
        saveBtn.setObjectName("saveBtn")
        saveBtn.clicked.connect(self._save)

        btnLayout.addWidget(cancelBtn)
        btnLayout.addWidget(saveBtn)
        layout.addLayout(btnLayout)

    def _buildThemesTab(self) -> QWidget:
        """Sestaví záložku s přepínači pro výběr barevného tématu."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        currentTheme = self.settings.get("theme")
        self._themeGroup = QButtonGroup(self)

        for key, theme in THEMES.items():
            row = QHBoxLayout()

            radio = QRadioButton(theme["name"])
            radio.setProperty("themeKey", key)
            radio.setChecked(key == currentTheme)
            radio.setStyleSheet("color: #f8f8f2;")
            self._themeGroup.addButton(radio)

            row.addWidget(radio)
            layout.addLayout(row)

        layout.addStretch()
        return widget

    def _buildShortcutsTab(self) -> QWidget:
        """Sestaví záložku s tabulkou pro úpravu klávesových zkratek."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)

        shortcuts = self.settings.get("shortcuts")
        labels = {
            "save": "Save file",
            "open_folder": "Open folder",
            "new_file": "New file",
            "split_editor": "Split editor",
            "close_split": "Close split",
        }

        self._shortcutTable = QTableWidget(len(shortcuts), 2)
        self._shortcutTable.setHorizontalHeaderLabels(["Action", "Shortcut"])
        self._shortcutTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self._shortcutTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self._shortcutTable.verticalHeader().setVisible(False)

        for row, (key, value) in enumerate(shortcuts.items()):
            actionItem = QTableWidgetItem(labels.get(key, key))
            actionItem.setFlags(Qt.ItemIsEnabled)
            actionItem.setForeground(QColor("#6272a4"))
            self._shortcutTable.setItem(row, 0, actionItem)

            shortcutItem = QTableWidgetItem(value)
            shortcutItem.setData(Qt.UserRole, key)
            self._shortcutTable.setItem(row, 1, shortcutItem)

        layout.addWidget(self._shortcutTable)
        return widget

    def _save(self) -> None:
        """Uloží nastavení z formuláře do SettingsManager a zavře dialog."""
        for btn in self._themeGroup.buttons():
            if btn.isChecked():
                self.settings.set("theme", btn.property("themeKey"))
                break

        shortcuts = {}
        for row in range(self._shortcutTable.rowCount()):
            key = self._shortcutTable.item(row, 1).data(Qt.UserRole)
            value = self._shortcutTable.item(row, 1).text()
            shortcuts[key] = value
        self.settings.set("shortcuts", shortcuts)

        self.settings.save()
        self.accept()
