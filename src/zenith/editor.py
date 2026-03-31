from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QPlainTextEdit
from PySide6.QtGui import QPainter, QColor, QTextFormat
from PySide6.QtCore import Qt, QRect, QSize
from .highlighter import Highlighter
import os

class lineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class codeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = lineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        
        self.updateLineNumberAreaWidth(0)
        self.lineNumberArea.show()
        self.lineNumberArea.raise_()

    def lineNumberAreaWidth(self):
        digits = 1
        maxValue = max(1, self.blockCount())
        while maxValue >= 10:
            maxValue /= 10
            digits += 1
        space = 15 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height())
        )
        self.lineNumberArea.raise_()

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#282a36"))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        painter.setFont(self.font())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#8be9fd"))
                
                rect = QRect(0, top, self.lineNumberArea.width() - 5, self.fontMetrics().height())
                painter.drawText(rect, Qt.AlignRight | Qt.AlignVCenter, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            blockNumber += 1

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

        self.textEdit = codeEditor()
        self.textEdit.setPlaceholderText("Start coding here...")
        self.textEdit.setFrameStyle(0)

        self.highlighter = Highlighter(self.textEdit.document())

        self.textEdit.setStyleSheet("""
            QPlainTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: none;
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