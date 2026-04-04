from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression, Qt

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#ff79c6"))
        keywordFormat.setFontWeight(QFont.Bold)

        keywords = ["def", "class", "import", "from", "if", "elif", "else", "try", "except", "finally", "return", "for", "while", "print", "pass", "break", "continue", "with", "as"]
        for word in keywords:
            pattern = QRegularExpression(rf"\b{word}\b")
            self.rules.append((pattern, keywordFormat, 0))

        nameFormat = QTextCharFormat()
        nameFormat.setForeground(QColor("#50fa7b")) 
        self.rules.append((QRegularExpression(r"\bclass\s+([A-Za-z_0-9]+)"), nameFormat, 1))
        self.rules.append((QRegularExpression(r"\bdef\s+([A-Za-z_0-9]+)"), nameFormat, 1))

        numberFormat = QTextCharFormat()
        numberFormat.setForeground(QColor("#bd93f9")) 
        self.rules.append((QRegularExpression(r"\b[0-9]+(\.[0-9]+)?\b"), numberFormat, 0))

        operatorFormat = QTextCharFormat()
        operatorFormat.setForeground(QColor("#ff79c6")) 
        self.rules.append((QRegularExpression(r"[\+\-\*\/\=\<\>\!\%\&\|\^]"), operatorFormat, 0))

        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor("#f1fa8c"))
        self.rules.append((QRegularExpression(r"\"[^\"]*\""), stringFormat, 0))
        self.rules.append((QRegularExpression(r"\'[^\']*\'"), stringFormat, 0))

        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor("#6272a4"))
        commentFormat.setFontItalic(True)
        self.rules.append((QRegularExpression(r"#[^\n]*"), commentFormat, 0))

        self.docstringFormat = QTextCharFormat()
        self.docstringFormat.setForeground(QColor("#f1fa8c"))

    def highlightBlock(self, text):
        for pattern, format, group in self.rules:
            matchIterator = pattern.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)