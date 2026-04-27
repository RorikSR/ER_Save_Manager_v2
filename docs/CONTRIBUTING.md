# Contributing

Thanks for helping improve the project.

## Recommended Flow

1. Create a fork.
2. Create a descriptive branch.
3. Keep changes small and testable.
4. Run tests.
5. Open a Pull Request.

## Minimum Tests

```powershell
python -m py_compile app.py SaveManager.py hexedit.py itemdata.py savefile_io.py os_layer.py logic\checksum.py logic\hex_editor.py logic\inventory_tools.py gui\main_window.py
python tools\test_checksum.py
```

## Important Rules

- Do not upload `.sl2` or `.co2` saves.
- Do not upload personal backups.
- Do not include personal paths in reports.
- Keep JSON catalogs readable.
- Any save-writing operation must create backups and validate checksum.

## Priority Areas

- Complete DLC catalog coverage.
- Continue moving legacy UI into separated modules.
- Harden safe mode and rollback behavior.
- Improve inventory scanning.
- Add automated tests.
