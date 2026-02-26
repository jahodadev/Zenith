from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeView, QFileSystemModel, QMessageBox
from PySide6.QtCore import QDir, Signal
from file_delegate import FileDelegate
import os

class Sidebar(QWidget):
    file_double_clicked = Signal(str)
    
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
        self.delegate = FileDelegate(self.tree)
        self.tree.setItemDelegate(self.delegate)
        self.delegate.trash_clicked.connect(self.delete_file)

        self.layout.addWidget(self.tree)

        self.setStyleSheet("background-color: #2c2c2c; cošlor: white;")

        self.tree.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index):
        file_path = self.model.filePath(index)
        if not self.model.isDir(index):
            self.file_double_clicked.emit(file_path)

    def delete_file(self, file_path):
        reply = QMessageBox.question(
            self,
            "Delete File",
            f"Are you sure you want to delete:\n{file_path}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                os.remove(file_path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete file:\n{e}")