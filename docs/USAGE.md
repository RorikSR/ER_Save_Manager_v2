# Usage Guide

## Before You Start

1. Close Elden Ring.
2. Make a manual backup of important saves.
3. Open `EldenRingSaveManager.exe`.
4. Set the game save folder through `Edit > Change Default Directory`.
5. Set your SteamID through `Edit > Change Default SteamID`.

## Vanilla And Seamless Co-op Modes

- Vanilla saves use `ER0000.sl2`.
- Seamless Co-op saves use `ER0000.co2`.
- Change mode through `File > Seamless Co-op Mode`.
- The dashboard shows the active mode.

## Create A Profile

1. Type a name in `New profile name`.
2. Click `Create profile from current save`.
3. The profile appears under `Saved Profiles`.

## Load A Profile

1. Select a profile under `Saved Profiles`.
2. Click `Load selected profile`.
3. The app backs up the current game save before overwriting it.

## Verify Current Save

Click `Verify current save` to inspect:

- Current extension.
- File size.
- Checksum.
- Detected slots.
- Character names.
- File MD5.

## Inventory Pro

`Inventory Pro` lets you browse the full item catalog.

You can filter by:

- Name.
- Category.
- Source: Base Game, DLC, or Custom.
- Goods ID.
- Raw ID.
- Internal IDs.

Available buttons:

- `Copy Goods ID`: copies the selected Goods ID.
- `Export catalog`: exports the current catalog to JSON.
- `Scan current save`: generates a real inventory report.
- `Edit quantities`: opens the Quantity Editor.

## Quantity Editor

The `Quantity Editor` modifies the current quantity of items already present in a character inventory.

Workflow:

1. Select a character.
2. Search for the item.
3. Select the item row.
4. Use `+1`, `+10`, `-1`, `-10`, or type an exact value.
5. Confirm the change.

The app:

- Writes to the exact selected inventory entry.
- Creates an automatic backup.
- Recalculates checksum.
- Verifies checksum after the change.

## Backup Browser

`Backup Browser` shows backups created by the app.

You can:

- View date, file, and MD5.
- Restore a backup.
- Open the backups folder.

Before restoring, the app creates a backup of the current save.

## Convert .sl2 / .co2

Use `Convert .sl2 / .co2` to convert between vanilla and Seamless Co-op formats.

The app:

- Asks for the source file.
- Asks for the destination path.
- Creates a backup if the destination already exists.
- Recalculates checksum.
- Verifies the result.
