# Zenith – Code Editor

Moderní, lehký a vizuálně přitažlivý textový editor pro programování. Postaven na **PySide6** s AST-based zvýrazňováním syntaxe přes **tree-sitter**.

## Funkce

- **Zvýrazňování syntaxe** – dynamické barvení kódu (klíčová slova, řetězce, čísla, komentáře, operátory) pomocí tree-sitter parseru
- **Čísla řádků** – vlastní panel s čísly řádků synchronizovaný se scrollováním
- **Správa souborů (Sidebar)** – stromová struktura složek a souborů s podporou vytvoření, otevření a smazání
- **Split view** – horizontální rozdělení editoru na více panelů (Ctrl+E), zavření aktivního panelu (Ctrl+W)
- **Více témat** – Dracula (výchozí), VS Code Dark+, Monokai
- **Nastavení** – dialog pro změnu tématu a přiřazení klávesových zkratek, uloženo do `~/.zenith/settings.json`
- **Ikony** – vizuální rozlišení typů souborů v sidebaru

## Klávesové zkratky

| Zkratka | Akce |
|---|---|
| Ctrl+S | Uložit soubor |
| Ctrl+O | Otevřít složku |
| Ctrl+N | Nový soubor |
| Ctrl+E | Rozdělit editor (nový panel) |
| Ctrl+W | Zavřít aktivní panel |

Všechny zkratky lze přenastavit v dialogu nastavení.

## Použité technologie

| Technologie | Verze |
|---|---|
| Python | ≥ 3.8 |
| PySide6 | 6.10.2 |
| tree-sitter | 0.25.2 |
| tree-sitter-python | 0.25.0 |

## Struktura projektu

```
editor-va/
├── src/zenith/
│   ├── __main__.py         # Vstupní bod (MainWindow, EditorArea)
│   ├── editor.py           # Widget editoru (codeEditor, Editor)
│   ├── sidebar.py          # Postranní panel se stromem souborů
│   ├── highlighter.py      # QSyntaxHighlighter (tree-sitter tokeny)
│   ├── lexer.py            # Tokenizer – tree-sitter Python parser
│   ├── themes.py           # Barevná témata
│   ├── settings_manager.py # Persistence nastavení (JSON)
│   ├── settings_dialog.py  # Dialog nastavení (téma, zkratky)
│   ├── file_delegate.py    # Vykreslování položek v stromu souborů
│   └── icons/              # PNG ikony
├── docs/                   # Vygenerovaná HTML dokumentace (Sphinx)
├── pyproject.toml          # Metadata projektu a vstupní bod
├── requirements.txt        # Závislosti
└── LICENSE
```

## Jak spustit

### 1. Klonování repozitáře

> Pokud již repozitář máte naklonovaný, tento krok přeskočte a přejděte do složky projektu.

```bash
git clone https://github.com/jahodadev/Zenith.git
cd Zenith
```

### 2. Virtuální prostředí

```bash
python -m venv venv
```

- **Windows:** `venv\Scripts\activate`
- **Linux / macOS:** `source venv/bin/activate`

### 3. Instalace závislostí

```bash
pip install -r requirements.txt
```

### 4. Spuštění

```bash
python -m zenith
```

Nebo nainstalovat jako balíček a spouštět příkazem `zenith`:

```bash
pip install .
zenith
```

## Nastavení uživatele

Nastavení (téma, zkratky) se ukládají do `~/.zenith/settings.json` a načítají se automaticky při každém spuštění.
