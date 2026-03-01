# Code Editor - Zenith

Projekt moderního, lehkého a vizuálně přitažlivého textového editoru určeného primárně pro programování. Aplikace je postavena na frameworku **PySide6** a zaměřuje se na přehlednost a uživatelský komfort.

## Hlavní funkce (Specifikace)

Tento editor bude obsahovat následující klíčové vlastnosti:

* **Zvýrazňování syntaxe:** Dynamické barvení kódu podle logických bloků (klíčová slova jako `if`, `for`, `def`, `class` atd.) pro lepší orientaci.
* **Kontrola syntaktických chyb:** Integrované podtrhávání chyb v reálném čase, které upozorní na překlepy nebo špatné odsazování.
* **Správa souborů (Sidebar):** Postranní panel se stromovou strukturou složek a souborů pro snadnou navigaci v projektu.
* **Multi-tab zobrazení:** Možnost mít otevřeno a upravovat více souborů současně v záložkách.
* **Číslování řádků:** Standardní prvek pro snadnou orientaci v kódu a ladění.
* **Vizuální styl a ikonky:** Moderní uživatelské rozhraní s ikonkami, které se mění podle typu souboru (např. logo Pythonu u `.py` souborů).

## Použité technologie

* **Jazyk:** Python
* **GUI Framework:** PySide6 (Qt for Python)
* **Další knihovny:** (budou doplňovány průběžně do requirements.txt)

## Struktura projektu

* `src/` - Zdrojové kódy aplikace.
  * `main.py` - Vstupní bod aplikace.
  * `editor.py` - Komponenta textového editoru.
  * `sidebar.py` - Postranní panel se stromem souborů.
  * `highlighter.py` - Zvýrazňovač syntaxe.
  * `file_delegate.py` - Delegát pro vykreslování položek v stromu souborů.
  * `icons/` - Ikony používané v aplikaci.
* `docs/` - Uživatelská dokumentace a další materiály.
* `requirements.txt` - Seznam závislostí pro instalaci.

## Jak spustit

1. Naklonujte repozitář a přejděte do složky projektu:
   ```
   git clone https://github.com/jahodadev/Zenith.git
   cd editor-va
   ```

2. Vytvořte a aktivujte virtuální prostředí:
   ```
   python -m venv venv
   ```
   - **Windows:** `venv\Scripts\activate`
   - **Linux / macOS:** `source venv/bin/activate`

3. Nainstalujte závislosti:
   ```
    
   ```

4. Spusťte aplikaci:
   ```
   python src/main.py
   ```
