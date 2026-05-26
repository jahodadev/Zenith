"""Syntaktický zvýrazňovač pro Python kód."""

from __future__ import annotations

from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from .themes import THEMES
from .lexer import tokenize_document, KEYWORD, NAME, NUMBER, STRING, COMMENT, OPERATOR


class Highlighter(QSyntaxHighlighter):
    """Zvýrazňuje Python tokeny barvami z aktuálního tématu."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._formats: dict[str, QTextCharFormat] = {}
        self._tokens_by_line: dict[int, list[tuple[str, int, int]]] = {}
        self._reparsing = False
        self.applyTheme(THEMES["dracula"])
        self.document().contentsChanged.connect(self._reparse)

    def applyTheme(self, theme: dict[str, str]) -> None:
        """Přestaví formáty barev podle nového tématu a znovu zvýrazní dokument."""
        def fmt(color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
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

    def _reparse(self) -> None:
        """Znovu tokenizuje celý dokument. Obsahuje ochranu proti zacyklení."""
        if self._reparsing:
            return
        self._reparsing = True
        text = self.document().toPlainText()
        self._tokens_by_line = tokenize_document(text)
        self.rehighlight()
        self._reparsing = False

    def highlightBlock(self, _text: str) -> None:
        """Aplikuje uložené formáty na aktuální blok textu."""
        line = self.currentBlock().blockNumber()
        for token_type, start, length in self._tokens_by_line.get(line, []):
            if token_type in self._formats:
                self.setFormat(start, length, self._formats[token_type])
