from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression, Qt

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#ff79c6"))
        keywordFormat.setFontWeight(QFont.Bold)

        keywords = ["def", "class", "import", "from", "if", "else", "return", "for", "while", "print"]
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}")
            self.rules.append((pattern, keywordFormat))
        
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#6272a4"))
        commentFormat.setFontItalic(True)
        self.rules.append((QRegularExpression(r"#[^\n]*"), commentFormat))

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#f1fa8c"))
        self.rules.append((QRegularExpression(r"\"[^\"]*\""), stringFormat))
        self.rules.append((QRegularExpression(r"\'[^\']*\'"), stringFormat))

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            matchIterator = pattern.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)