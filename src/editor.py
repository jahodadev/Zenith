from PySide6.QtWidgets import QTextEdit
from highlighter import Highlighter

class Editor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Start coding here...")

        self.highlighter = Highlighter(self.document())

        self.setStyleSheet("""
            QTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
            }
        """)