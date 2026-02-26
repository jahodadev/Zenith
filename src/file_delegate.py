from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QIcon
from PySide6.QtCore import QRect, Qt, Signal, QObject, QEvent

class FileDelegate(QStyledItemDelegate):
    trash_clicked = Signal(str)  # Custom signal

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trash_icon = QIcon("src/icons/trash.png")  # Adjust path as needed

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.column() == 0:
            rect = option.rect
            icon_size = 16
            margin = 4
            icon_rect = QRect(
                rect.right() - icon_size - margin,
                rect.center().y() - icon_size // 2,
                icon_size,
                icon_size
            )
            self.trash_icon.paint(painter, icon_rect, Qt.AlignCenter)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease and index.column() == 0:
            rect = option.rect
            icon_size = 16
            margin = 4
            icon_rect = QRect(
                rect.right() - icon_size - margin,
                rect.center().y() - icon_size // 2,
                icon_size,
                icon_size
            )
            if icon_rect.contains(event.pos()):
                file_path = model.filePath(index)
                self.trash_clicked.emit(file_path)
                return True
        return super().editorEvent(event, model, option, index)