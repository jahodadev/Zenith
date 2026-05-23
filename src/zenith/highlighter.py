from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from .themes import THEMES
from .lexer import tokenize_document, KEYWORD, NAME, NUMBER, STRING, COMMENT, OPERATOR

class Highlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._formats = {}
        self._tokens_by_line = {}
        self._reparsing = False
        self.applyTheme(THEMES["dracula"])
        self.document().contentsChanged.connect(self._reparse)

    def applyTheme(self, theme):
        def fmt(color, bold=False, italic=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Bold)
            if italic:
                f.setFontItalic(True)
            return f

        self._formats = {
            KEYWORD:  fmt(theme["keyword"], bold=True),
            NAME:     fmt(theme["function_name"]),
            NUMBER:   fmt(theme["number"]),
            STRING:   fmt(theme["string"]),
            COMMENT:  fmt(theme["comment"], italic=True),
            OPERATOR: fmt(theme["operator"]),
        }
        self._reparse()

    def _reparse(self):
        if self._reparsing:
            return
        self._reparsing = True
        text = self.document().toPlainText()
        self._tokens_by_line = tokenize_document(text)
        self.rehighlight()
        self._reparsing = False

    def highlightBlock(self, _text):
        line = self.currentBlock().blockNumber()
        for token_type, start, length in self._tokens_by_line.get(line, []):
            if token_type in self._formats:
                self.setFormat(start, length, self._formats[token_type])
