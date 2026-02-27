from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QIcon
from PySide6.QtCore import QRect, Qt, Signal, QObject, QEvent

class FileDelegate(QStyledItemDelegate):
    trashClicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.trashIcon = QIcon("src/icons/trash.png")

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.column() == 0:
            rect = option.rect
            iconSize = 16
            margin = 4
            iconRect = QRect(
                rect.right() - iconSize - margin,
                rect.center().y() - iconSize // 2,
                iconSize,
                iconSize
            )
            self.trashIcon.paint(painter, iconRect, Qt.AlignCenter)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease and index.column() == 0:
            rect = option.rect
            iconSize = 16
            margin = 4
            iconRect = QRect(
                rect.right() - iconSize - margin,
                rect.center().y() - iconSize // 2,
                iconSize,
                iconSize
            )
            if iconRect.contains(event.pos()):
                filePath = model.filePath(index)
                self.trashClicked.emit(filePath)
                return True
        return super().editorEvent(event, model, option, index)