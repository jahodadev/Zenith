from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
from PySide6.QtCore import Qt
from highlighter import Highlighter
import os

class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.current_file = None
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0) # Žádné mezery u okrajů
        self.main_layout.setSpacing(0)

        self.toolbar = QWidget()
        self.toolbar.setFixedHeight(35)
        self.toolbar.setStyleSheet("background-color: #21222c; border-bottom: 1px solid #191a21;")

        self.toolbar_layout = QHBoxLayout(self.toolbar)
        self.toolbar_layout.setContentsMargins(10, 0, 10, 0)

        self.file_label = QLabel("untitled.py")
        self.file_label.setStyleSheet("color: #6272a4; font-size: 12px;")

        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(60, 25)
        self.save_btn.setStyleSheet("""
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

        self.toolbar_layout.addWidget(self.file_label)
        self.toolbar_layout.addStretch()
        self.toolbar_layout.addWidget(self.save_btn)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Start coding here...")
        self.text_edit.setFrameStyle(0)

        self.highlighter = Highlighter(self.text_edit.document())

        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #282a36;
                color: #f8f8f2;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                padding: 10px;
            }
        """)

        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.text_edit)

        self.save_btn.clicked.connect(self.save_file)

        def update_header(self):
            if self.current_file:
                name = os.path.basename(self.current_file)
                self.file_label.setText(name)
            else:
                self.file_label.setText("untitled.py")

    def save_file(self):
        if not self.current_file:
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Save File", 
                "", 
                "Python Files (*.py);;All Files (*)"
            )
            if file_path:
                self.current_file = file_path
            else:
                return

        try:
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())
            
            self.update_header()
            print(f"Uloženo do: {self.current_file}")
            
        except Exception as e:
            print(f"Chyba při ukládání: {e}")

    def open_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            self.text_edit.setPlainText(content)
            self.current_file = file_path
            self.update_header()
            print(f"Otevřeno: {file_path}")
        except Exception as e:
            print(f"Chyba při otevírání: {e}")

    def update_header(self):
        if self.current_file:
            name = os.path.basename(self.current_file)
            self.file_label.setText(name)
        else:
            self.file_label.setText("Untilted file")