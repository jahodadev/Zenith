from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileSystemModel, QMessageBox, QPushButton, QFileDialog, QInputDialog, QLabel
from PySide6.QtCore import QDir, Signal, QSize
from PySide6.QtGui import QIcon, QImage, QColor, QPixmap
from .file_delegate import FileDelegate
import os

def createColoredIcon(iconPath, colorHex="#8be9fd"):
    img = QImage(iconPath)
    if img.isNull():
        return QIcon()
        
    img = img.convertToFormat(QImage.Format_ARGB32)
    targetColor = QColor(colorHex)
    
    for y in range(img.height()):
        for x in range(img.width()):
            c = img.pixelColor(x, y)
            if c.alpha() > 200:
                targetColor.setAlpha(255)
                img.setPixelColor(x, y, targetColor)
            else:
                img.setPixelColor(x, y, QColor(0, 0, 0, 0))
                
    return QIcon(QPixmap.fromImage(img))

class Sidebar(QWidget):
    fileDoubleClicked = Signal(str)
    saveFileClicked = Signal()
    settingsClicked = Signal()
    
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
        self.toolbarLayout.setSpacing(5)

        iconStyle = """
            QPushButton {
                background: transparent; 
                border: none;
                color: #8be9fd; 
                border-radius: 4px; 
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #44475a; 
            }
            QPushButton:pressed {
                background-color: #6272a4;
            }
        """

        baseDir = os.path.dirname(os.path.abspath(__file__))
        iconsDir = os.path.join(baseDir, "icons")

        self.newFileButton = QPushButton()
        self.newFileButton.setIcon(createColoredIcon(os.path.join(iconsDir, "new-document.png")))
        self.newFileButton.setIconSize(QSize(16, 16))
        self.newFileButton.setFixedSize(22, 22)
        self.newFileButton.setToolTip("New File")
        self.newFileButton.setStyleSheet(iconStyle)

        self.openFolderButton = QPushButton()
        self.openFolderButton.setIcon(createColoredIcon(os.path.join(iconsDir, "folder.png")))
        self.openFolderButton.setIconSize(QSize(16, 16))
        self.openFolderButton.setFixedSize(22, 22)
        self.openFolderButton.setToolTip("Open Folder")
        self.openFolderButton.setStyleSheet(iconStyle)

        self.saveFileButton = QPushButton()
        self.saveFileButton.setIcon(createColoredIcon(os.path.join(iconsDir, "diskette.png")))
        self.saveFileButton.setIconSize(QSize(16, 16))
        self.saveFileButton.setFixedSize(22, 22)
        self.saveFileButton.setToolTip("Save File")
        self.saveFileButton.setStyleSheet(iconStyle)

        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(createColoredIcon(os.path.join(iconsDir, "settings.png")))
        self.settingsButton.setIconSize(QSize(16, 16))
        self.settingsButton.setFixedSize(22, 22)
        self.settingsButton.setToolTip("Settings")
        self.settingsButton.setStyleSheet(iconStyle)

        self.toolbarLayout.addWidget(self.newFileButton)
        self.toolbarLayout.addWidget(self.openFolderButton)
        self.toolbarLayout.addWidget(self.saveFileButton)
        self.toolbarLayout.addStretch()
        self.toolbarLayout.addWidget(self.settingsButton)

        self.layout.addWidget(self.toolbar)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath())

        currentFolderName = os.path.basename(QDir.currentPath())
        self.folderLabel = QLabel(currentFolderName.upper())
        self.folderLabel.setStyleSheet("color: #6272a4; font-size: 11px; font-weight: bold; padding: 10px 10px 5px 10px; margin: 0px; background-color: #1e1f29; border: none;")
        self.layout.addWidget(self.folderLabel)

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

        self.setStyleSheet("background-color: #1e1f29; color: white;")
        self.tree.setStyleSheet("QTreeView { background-color: #1e1f29; color: white; border: none; }")

        self.tree.doubleClicked.connect(self.onDoubleClick)
        
        self.newFileButton.clicked.connect(self.createNewFile)
        self.openFolderButton.clicked.connect(self.chooseFolder)
        self.saveFileButton.clicked.connect(self.saveFileClicked.emit)
        self.settingsButton.clicked.connect(self.settingsClicked.emit)

        self.layout.addWidget(self.tree)

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
            self.folderLabel.setText(os.path.basename(folderPath).upper())

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
                with open(filePath, "w", encoding="utf-8"):
                    print(f"File was successfully created: {filePath}")
            except Exception as e:
                print(f"Error while creating a new file: {e}")