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

- [ ] Link `docs/RELEASE_NOTES_v1.0.0-sote.md` or copy its relevant notes into the GitHub Release body.
- [ ] Include the safety warning about backups, offline use, and ban risk.
- [ ] Confirm `LICENSE`, `CREDITS.md`, `NOTICE.md`, `SECURITY.md`, and `SUPPORT.md` are present.

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
