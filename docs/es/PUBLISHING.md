# Publicacion En GitHub

## Preparar El Repositorio

1. Revisa que no haya saves personales:

```powershell
Get-ChildItem -Recurse -Include *.sl2,*.co2,ER0000.* | Select-Object FullName
```

2. Revisa que no se suban builds:

```powershell
Get-ChildItem build,dist -ErrorAction SilentlyContinue
```

3. Confirma que `.gitignore` este activo.

## Primer Push

Desde la carpeta del proyecto:

```powershell
git init
git add .
git status
git commit -m "Initial Shadow of the Erdtree save manager release"
git branch -M main
git remote add origin https://github.com/RorikSR/ER_Save_Manager_v2.git
git push -u origin main
```

Si el proyecto ya tiene un remoto `origin`:

```powershell
git remote set-url origin https://github.com/RorikSR/ER_Save_Manager_v2.git
git push -u origin main
```

Antes de `git commit`, revisa que no aparezcan:

- Saves `.sl2` / `.co2`.
- Backups personales.
- Reportes con rutas personales.
- `dist/` o `build/`.

## Crear Release

1. Compila:

```powershell
.\build_exe.ps1
```

2. Prueba:

```powershell
python tools\test_checksum.py
```

3. En GitHub, ve a `Releases > Draft a new release`.
   Pagina de releases: https://github.com/RorikSR/ER_Save_Manager_v2/releases
4. Usa un tag como:

```text
v1.8.0-sote
```

5. Adjunta:

```text
dist/EldenRingSaveManager.exe
```

6. Copia la plantilla de `docs/RELEASE_CHECKLIST.md`.

## Nombre Del Repositorio

```text
ER_Save_Manager_v2
```

## Descripcion Corta Para GitHub

```text
Elden Ring save manager with Shadow of the Erdtree item catalog, .sl2/.co2 support, checksum validation, backups, Inventory Pro and Quantity Editor.
```

## Topics Sugeridos

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
