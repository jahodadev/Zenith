from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression, Qt

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#ff79c6"))
        keyword_format.setFontWeight(QFont.Bold)

        keywords = ["def", "class", "import", "from", "if", "else", "return", "for", "while", "print"]
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}")
            self.rules.append((pattern, keyword_format))
        
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6272a4"))
        comment_format.setFontItalic(True)
        self.rules.append((QRegularExpression(r"#[^\n]*"), comment_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#f1fa8c"))
        self.rules.append((QRegularExpression(r"\"[^\"]*\""), string_format))
        self.rules.append((QRegularExpression(r"\'[^\']*\'"), string_format))

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)