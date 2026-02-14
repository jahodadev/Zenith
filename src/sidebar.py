from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel
from PySide6.QtCore import QDir

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.currentPath()))

        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setHeaderHidden(True)

        self.layout.addWidget(self.tree)

        self.setStyleSheet("background-color: #2c2c2c; color: white;")