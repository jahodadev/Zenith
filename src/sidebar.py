from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileSystemModel, QMessageBox, QPushButton, QFileDialog, QInputDialog
from PySide6.QtCore import QDir, Signal
from file_delegate import FileDelegate
import os

class Sidebar(QWidget):
    fileDoubleClicked = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(200)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.setSpacing(0)

        self.toolbar = QWidget()
        self.toolbar.setFixedHeight(35)
        self.toolbar.setStyleSheet("background-color: #21222c; border-bottom: 1px solid #191a21;")

        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setContentsMargins(10, 0, 10, 0)

        self.openBtn = QPushButton("Open Folder")
        self.openBtn.setFixedHeight(25)
        self.openBtn.setStyleSheet("""
            QPushButton {
                background-color: #44475a;
                color: #f8f8f2;
                border-radius: 4px;
                font-weight: bold;
                padding: 0 10px;
            }
            QPushButton:hover {
                background-color: #6272a4;
            }
        """)

        self.toolbarLayout.addWidget(self.openBtn)
        self.toolbarLayout.addStretch()

        self.layout.addWidget(self.toolbar)

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
        self.delegate.trashClicked.connect(self.deleteFile)

        self.setStyleSheet("background-color: #2c2c2c; color: white;")

        self.tree.doubleClicked.connect(self.onDoubleClick)
        self.openBtn.clicked.connect(self.chooseFolder)

        self.fileOpsBar = QWidget()
        self.fileOpsBar.setFixedHeight(30)
        self.fileOpsBar.setStyleSheet("background-color: #21222c;")

        self.fileOpsLayout = QHBoxLayout(self.fileOpsBar)
        self.fileOpsLayout.setContentsMargins(10, 0, 10, 0)
        self.fileOpsLayout.setSpacing(5)

        self.newFileButton = QPushButton("+")
        self.newFileButton.setFixedSize(22, 22)
        self.newFileButton.setToolTip("New File")

        self.newFileButton.setStyleSheet("""
            QPushButton {
                background-color: transparent; 
                color: #8be9fd; 
                border-radius: 4px; 
                font-size: 16px;
                font-weight: bold;
                padding-bottom: 2px; 
            }
            QPushButton:hover {
                background-color: #44475a; 
            }
            QPushButton:pressed {
                background-color: #6272a4;
            }
        """)

        self.fileOpsLayout.addWidget(self.newFileButton)

        self.fileOpsLayout.addStretch()
        self.layout.addWidget(self.fileOpsBar)

        self.layout.addWidget(self.tree)

        self.newFileButton.clicked.connect(self.createNewFile)

    def onDoubleClick(self, index):
        filePath = self.model.filePath(index)
        if not self.model.isDir(index):
            self.fileDoubleClicked.emit(filePath)

    def deleteFile(self, filePath):
        reply = QMessageBox.question(
            self,
            "Delete File",
            f"Are you sure you want to delete:\n{filePath}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                os.remove(filePath)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not delete file:\n{e}")

    def chooseFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, "Choose project's folder")

        if folderPath:
            self.model.setRootPath(folderPath)
            self.tree.setRootIndex(self.model.index(folderPath))

    def createNewFile(self):
        indexes = self.tree.selectedIndexes()
        if indexes: 
            index = indexes[0]
            if not self.model.isDir(index):
                index = index.parent()
            targetDir = self.model.filePath(index)
        else:
            targetDir = self.model.rootPath()
        
        fileName, ok = QInputDialog.getText(self, "New File", "Enter file name:")

        if fileName and ok:
            filePath = os.path.join(targetDir, fileName)
            try:
                with open(filePath, "w", encoding="utf-8") as f:
                    print(f"File was successfully created: {filePath}")
            except Exception as e:
                print(f"Error while creating a new file: {e}")