# Safety, Backups And Checksum

## Main Rule

Do not edit saves while Elden Ring is running.

## Automatic Backups

Write operations create automatic backups in:

```text
data/backups/
```

Legacy tools may also use:

```text
data/archive/
data/backup/
```

These folders contain local data and must not be uploaded to GitHub.

## Checksum

The project recalculates and verifies internal MD5 checksums.

Main checksum code:

```text
logic/checksum.py
```

Recommended test:

```powershell
python tools\test_checksum.py
```

Expected result:

- `before_valid: True`
- `after_once_valid: True`
- `after_twice_valid: True`
- `idempotent: True`

## Manual Rollback

If something goes wrong:

1. Close the app.
2. Open `data/backups/`.
3. Copy the correct backup.
4. Replace `ER0000.sl2` or `ER0000.co2` in the game save folder.
5. Open the app and run `Verify current save`.

## Online / Anti-Cheat

Using modified saves online may carry risk. The safest recommendation is:

- Edit offline.
- Keep clean backups.
- Avoid impossible items or absurd quantities.
- Do not mix modified saves with online play unless you understand the consequences.
