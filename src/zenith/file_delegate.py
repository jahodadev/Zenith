from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QIcon, QImage, QColor, QPixmap
from PySide6.QtCore import QRect, Qt, Signal, QObject, QEvent
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

class FileDelegate(QStyledItemDelegate):
    trashClicked = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        currentDir = os.path.dirname(os.path.abspath(__file__))
        iconPath = os.path.join(currentDir, "icons", "recycle-bin.png")
        self.trashIcon = createColoredIcon(iconPath, "#ff5555")

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