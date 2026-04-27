# Release Checklist

## Before Building

- [ ] Close Elden Ring.
- [ ] Check that no personal saves are in the repository.
- [ ] Check that `data/config.json` is not staged.
- [ ] Run syntax checks.
- [ ] Run `python tools\test_checksum.py`.
- [ ] Test `python app.py`.

## Build

```powershell
.\build_exe.ps1
```

## Executable Test

- [ ] Open `dist\EldenRingSaveManager.exe`.
- [ ] Confirm it opens without traceback.
- [ ] Confirm it creates/uses `dist\data`.
- [ ] Test `Verify current save`.
- [ ] Test `Inventory Pro`.
- [ ] Test `Quantity Editor` on a copy of a save.
- [ ] Confirm checksum remains valid.

## Release Notes

### Summary

- Shadow of the Erdtree support.
- `.sl2` and `.co2` support.
- Current-save dashboard.
- Inventory Pro.
- Quantity Editor.
- Backup Browser.
- Checksum verification and recalculation.

### Warnings

- Use at your own risk.
- Keep manual backups.
- Do not edit saves while the game is running.
- Do not upload personal saves in bug reports.

## Artifacts

Attach to GitHub Release:

```text
dist\EldenRingSaveManager.exe
```
