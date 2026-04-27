# Development Guide

## Requirements

- Python 3.11+
- Windows 10/11 for `.exe` builds
- Python with Tk/Tcl support

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Development dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

## Run

```powershell
python app.py
```

Or:

```powershell
.\run_app.ps1
```

## Build

```powershell
.\build_exe.ps1
```

Output:

```text
dist/EldenRingSaveManager.exe
```

## Recommended Tests

Syntax check:

```powershell
python -m py_compile app.py SaveManager.py hexedit.py itemdata.py savefile_io.py os_layer.py logic\checksum.py logic\hex_editor.py logic\inventory_tools.py gui\main_window.py
```

Checksum:

```powershell
python tools\test_checksum.py
```

Catalog:

```powershell
python -c "from logic import inventory_tools; print(len(inventory_tools.catalog_rows()))"
```

Inventory scanner:

```powershell
python tools\scan_inventory.py
```

## Architecture

The project still contains legacy UI code in `SaveManager.py`, but new logic is being moved into packages:

```text
gui/                    Visual helpers and theme
logic/checksum.py       Checksum verification/recalculation
logic/hex_editor.py     Facade over legacy hexedit.py
logic/inventory_tools.py Catalog, scanning and quantity editing helpers
savefile_io.py          Paths, conversions and backups
app_paths.py            Source/PyInstaller compatible paths
```

## Item Data

Items are loaded from JSON:

```text
data/items/base_game.json
data/items/shadow_of_the_erdtree.json
```

Recommended format:

```json
{
  "Consumables": {
    "Scadutree Fragment": {
      "ids": [144, 171],
      "goods_id": 2010000,
      "raw_item": 2954800016,
      "source": "Shadow of the Erdtree"
    }
  }
}
```

## Do Not Commit

Do not commit:

- `dist/`
- `build/`
- `data/save-files/`
- `data/backups/`
- `data/reports/`
- `*.sl2`
- `*.co2`
- `data/config.json`
