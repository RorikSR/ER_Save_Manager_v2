# Contribuir

Gracias por querer mejorar el proyecto.

## Flujo Recomendado

1. Crea un fork.
2. Crea una rama descriptiva.
3. Haz cambios pequenos y testeables.
4. Ejecuta pruebas.
5. Abre Pull Request.

## Pruebas Minimas

```powershell
python -m py_compile app.py SaveManager.py hexedit.py itemdata.py savefile_io.py os_layer.py logic\checksum.py logic\hex_editor.py logic\inventory_tools.py gui\main_window.py
python tools\test_checksum.py
```

## Reglas Importantes

- No subir saves `.sl2` o `.co2`.
- No subir backups personales.
- No incluir rutas personales en reportes.
- Mantener catalogos JSON legibles.
- Toda operacion de escritura debe crear backup y validar checksum.

## Areas Prioritarias

- Completar catalogo DLC.
- Mejorar migracion de UI legacy a componentes separados.
- Endurecer modo seguro/rollback.
- Mejorar escaneo de inventario.
- Agregar tests automatizados.
