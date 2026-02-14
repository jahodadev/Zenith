from PySide6.QtWidgets import QTextEdit

class Editor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("Start coding here")