# Guia De Desarrollo

## Requisitos

- Python 3.11+
- Windows 10/11 para build `.exe`
- Tk/Tcl incluido con Python

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Dependencias de desarrollo:

```powershell
python -m pip install -r requirements-dev.txt
```

## Ejecutar

```powershell
python app.py
```

O:

```powershell
.\run_app.ps1
```

## Compilar

```powershell
.\build_exe.ps1
```

Salida:

```text
dist/EldenRingSaveManager.exe
```

## Pruebas Recomendadas

Compilacion sintactica:

```powershell
python -m py_compile app.py SaveManager.py hexedit.py itemdata.py savefile_io.py os_layer.py logic\checksum.py logic\hex_editor.py logic\inventory_tools.py gui\main_window.py
```

Checksum:

```powershell
python tools\test_checksum.py
```

Catalogo:

```powershell
python -c "from logic import inventory_tools; print(len(inventory_tools.catalog_rows()))"
```

Escaner de inventario:

```powershell
python tools\scan_inventory.py
```

## Arquitectura

El proyecto aun conserva UI legacy en `SaveManager.py`, pero la logica nueva se esta moviendo a paquetes:

```text
gui/                 Helpers visuales y tema
logic/checksum.py    Verificacion/recalculo checksum
logic/hex_editor.py  Fachada hacia hexedit.py
logic/inventory_tools.py Catalogo, escaneo y editor de cantidades
savefile_io.py       Rutas, conversiones y backups
app_paths.py         Rutas compatibles con fuente y PyInstaller
```

## Datos De Items

Los items se cargan desde JSON:

```text
data/items/base_game.json
data/items/shadow_of_the_erdtree.json
```

Formato recomendado:

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

## No Committear

No subas:

- `dist/`
- `build/`
- `data/save-files/`
- `data/backups/`
- `data/reports/`
- `*.sl2`
- `*.co2`
- `data/config.json`
