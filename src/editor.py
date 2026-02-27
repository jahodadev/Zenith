from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PySide6.QtCore import Qt
from highlighter import Highlighter
import os

class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.currentFile = None
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.toolbar = QWidget()
        self.toolbar.setFixedHeight(35)
        self.toolbar.setStyleSheet("background-color: #21222c; border-bottom: 1px solid #191a21;")

        self.toolbarLayout = QHBoxLayout(self.toolbar)
        self.toolbarLayout.setContentsMargins(10, 0, 10, 0)

        self.fileLabel = QLabel("untitled.py")
        self.fileLabel.setStyleSheet("color: #6272a4; font-size: 12px;")

        self.saveBtn = QPushButton("Save")
        self.saveBtn.setFixedSize(60, 25)
        self.saveBtn.setStyleSheet("""
            QPushButton {
                background-color: #44475a;
                color: #f8f8f2;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6272a4;
            }
        """)

        self.toolbarLayout.addWidget(self.fileLabel)
        self.toolbarLayout.addStretch()
        self.toolbarLayout.addWidget(self.saveBtn)

        self.textEdit = QTextEdit()
        self.textEdit.setPlaceholderText("Start coding here...")
        self.textEdit.setFrameStyle(0)

        self.highlighter = Highlighter(self.textEdit.document())

        self.textEdit.setStyleSheet("""
            QTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                padding: 10px;
            }
        """)

        self.mainLayout.addWidget(self.toolbar)
        self.mainLayout.addWidget(self.textEdit)

        self.saveBtn.clicked.connect(self.saveFile)

        def updateHeader(self):
            if self.currentFile:
                name = os.path.basename(self.currentFile)
                self.fileLabel.setText(name)
            else:
                self.fileLabel.setText("untitled.py")

    def saveFile(self):
        if not self.currentFile:
            filePath, _ = QFileDialog.getSaveFileName(
                self, 
                "Save File", 
                "", 
                "Python Files (*.py);;All Files (*)"
            )
            if filePath:
                self.currentFile = filePath
            else:
                return

        try:
            with open(self.currentFile, "w", encoding="utf-8") as f:
                f.write(self.textEdit.toPlainText())
            
            self.updateHeader()
            print(f"Uloženo do: {self.currentFile}")
            
        except Exception as e:
            print(f"Chyba při ukládání: {e}")

    def openFile(self, filePath):
        try:
            with open(filePath, "r", encoding="utf-8") as f:
                content = f.read()

            self.textEdit.setPlainText(content)
            self.currentFile = filePath
            self.updateHeader()
            print(f"Otevřeno: {filePath}")
        except Exception as e:
            print(f"Chyba při otevírání: {e}")

    def updateHeader(self):
        if self.currentFile:
            name = os.path.basename(self.currentFile)
            self.fileLabel.setText(name)
        else:
            self.fileLabel.setText("Untilted file")