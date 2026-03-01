import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QSplitter
from PySide6.QtCore import Qt
from editor import Editor
from sidebar import Sidebar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zenith - Code Editor")
        self.resize(1000, 700)

        self.splitter = QSplitter(Qt.Horizontal)

        self.sidebar = Sidebar()
        self.editor = Editor()

        self.sidebar.fileDoubleClicked.connect(self.editor.openFile)

        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.editor)

        self.splitter.setSizes([200, 800])

        self.setCentralWidget(self.splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())