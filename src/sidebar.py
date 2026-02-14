from PySide6.QtWidgets import QWidget

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(200)
        self.setStyleSheet("background-color: #2c2c2c;")