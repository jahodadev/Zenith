import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QSplitter, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence
from .editor import Editor
from .sidebar import Sidebar

class EditorArea(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet(
            "QSplitter::handle {background-color: #191a21;}"
        )
        layout.addWidget(self.splitter)

        self.editors = []

        self.addEditor()

    def addEditor(self):
        editor = Editor()
        self.editors.append(editor)
        self.splitter.addWidget(editor)
        count = len(self.editors)
        self.splitter.setSizes([1000 // count] * count)
        return editor

    def closeActiveEditor(self):
        if len(self.editors) <= 1:
            return
        editor = self._getActiveEditor()
        if editor:
            self.editors.remove(editor)
            editor.deleteLater()

    def openFile(self, filePath):
        editor = self._getActiveEditor()
        if editor:
            editor.openFile(filePath)

    def saveFile(self):
        editor = self._getActiveEditor()
        if editor:
            editor.saveFile()

    def _getActiveEditor(self):
        for editor in self.editors:
            if editor.textEdit.hasFocus():
                return editor
        if self.editors:
            return self.editors[0]
        else:
            return None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zenith - Code Editor")
        self.resize(1000, 700)

        self.splitter = QSplitter(Qt.Horizontal)

        self.sidebar = Sidebar()
        self.editor = EditorArea()

        self.sidebar.fileDoubleClicked.connect(self.editor.openFile)
        self.sidebar.saveFileClicked.connect(self.editor.saveFile)

        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.editor)

        self.splitter.setSizes([200, 800])
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #191a21; }")

        self.setCentralWidget(self.splitter)

        splitAction = QAction(self)
        splitAction.setShortcut(QKeySequence("Ctrl+E"))
        splitAction.triggered.connect(self.editor.addEditor)
        self.addAction(splitAction)

        closeAction = QAction(self)
        closeAction.setShortcut(QKeySequence("Ctrl+W"))
        closeAction.triggered.connect(self.editor.closeActiveEditor)
        self.addAction(closeAction)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()