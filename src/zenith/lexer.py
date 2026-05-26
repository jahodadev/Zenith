"""Tokenizátor Python kódu pomocí tree-sitter."""

from __future__ import annotations

import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

KEYWORD  = "keyword"
NAME     = "name"
NUMBER   = "number"
STRING   = "string"
COMMENT  = "comment"
OPERATOR = "operator"

KEYWORD_TYPES = {
    "def", "class", "import", "from", "if", "elif", "else", "try", "except",
    "finally", "return", "for", "while", "pass", "break", "continue", "with",
    "as", "and", "or", "not", "in", "is", "lambda", "yield", "raise",
    "True", "False", "None", "del", "global", "assert", "async", "await",
}


def tokenize_document(text: str) -> dict[int, list[tuple[str, int, int]]]:
    """Naparsuje zdrojový kód a vrátí tokeny rozdělené podle řádků.

    Vrací slovník kde klíč je číslo řádku a hodnota je seznam trojic
    (typ tokenu, začáteční sloupec, délka).
    """
    tree = parser.parse(text.encode("utf-8"))
    tokens_by_line: dict[int, list[tuple[str, int, int]]] = {}

    def walk(node) -> None:
        if node.child_count == 0 and node.start_point[0] == node.end_point[0]:
            line   = node.start_point[0]
            start  = node.start_point[1]
            length = node.end_point[1] - start

            if node.type in KEYWORD_TYPES:
                token_type = KEYWORD
            elif node.type == "identifier":
                token_type = NAME
            elif node.type in ("integer", "float"):
                token_type = NUMBER
            elif node.type == "string":
                token_type = STRING
            elif node.type == "comment":
                token_type = COMMENT
            elif node.type in ("+", "-", "*", "/", "=", "<", ">", "!", "%", "|", "&"):
                token_type = OPERATOR
            else:
                return

            if line not in tokens_by_line:
                tokens_by_line[line] = []
            tokens_by_line[line].append((token_type, start, length))

        for child in node.children:
            walk(child)

    walk(tree.root_node)
    return tokens_by_line
