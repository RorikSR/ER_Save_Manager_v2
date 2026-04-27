# Publishing On GitHub

## Prepare The Repository

1. Check for personal save files:

```powershell
Get-ChildItem -Recurse -Include *.sl2,*.co2,ER0000.* | Select-Object FullName
```

2. Check that build folders are not staged:

```powershell
Get-ChildItem build,dist -ErrorAction SilentlyContinue
```

3. Confirm `.gitignore` is active.

## First Push

From the project folder:

```powershell
git init
git add .
git status
git commit -m "Initial Shadow of the Erdtree save manager release"
git branch -M main
git remote add origin https://github.com/RorikSR/ER_Save_Manager_v2.git
git push -u origin main
```

If the project already has an `origin` remote:

```powershell
git remote set-url origin https://github.com/RorikSR/ER_Save_Manager_v2.git
git push -u origin main
```

Before `git commit`, make sure these are not staged:

- `.sl2` / `.co2` saves.
- Personal backups.
- Reports with personal paths.
- `dist/` or `build/`.

## Create A Release

1. Build:

```powershell
.\build_exe.ps1
```

2. Test:

```powershell
python tools\test_checksum.py
```

3. In GitHub, open `Releases > Draft a new release`.
   Release page: https://github.com/RorikSR/ER_Save_Manager_v2/releases
4. Use a tag like:

```text
v1.8.0-sote
```

5. Attach:

```text
dist/EldenRingSaveManager.exe
```

6. Use the checklist in `docs/RELEASE_CHECKLIST.md`.

## Repository Name

```text
ER_Save_Manager_v2
```

## Short GitHub Description

```text
Elden Ring save manager with Shadow of the Erdtree item catalog, .sl2/.co2 support, checksum validation, backups, Inventory Pro and Quantity Editor.
```

## Suggested Topics

```text
elden-ring
save-editor
save-manager
shadow-of-the-erdtree
seamless-coop
python
tkinter
pyinstaller
modding-tools
```
