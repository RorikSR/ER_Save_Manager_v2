# Release Checklist

## Antes De Compilar

- [ ] Cerrar Elden Ring.
- [ ] Verificar que no haya saves personales en el repo.
- [ ] Verificar que `data/config.json` no se va a commitear.
- [ ] Ejecutar compilacion sintactica.
- [ ] Ejecutar `python tools\test_checksum.py`.
- [ ] Probar `python app.py`.

## Build

```powershell
.\build_exe.ps1
```

## Prueba Del Ejecutable

- [ ] Abrir `dist\EldenRingSaveManager.exe`.
- [ ] Confirmar que abre sin traceback.
- [ ] Confirmar que crea/usa `dist\data`.
- [ ] Probar `Verify current save`.
- [ ] Probar `Inventory Pro`.
- [ ] Probar `Quantity Editor` sobre una copia de save.
- [ ] Confirmar que el checksum queda valido.

## Release Notes

- [ ] Enlazar `docs/RELEASE_NOTES_v1.0.0-sote.md` o copiar sus notas relevantes en la descripcion de GitHub Release.
- [ ] Incluir advertencia de seguridad sobre backups, uso offline y riesgo de ban.
- [ ] Confirmar que existen `LICENSE`, `CREDITS.md`, `NOTICE.md`, `SECURITY.md` y `SUPPORT.md`.

### Resumen

- Soporte Shadow of the Erdtree.
- Soporte `.sl2` y `.co2`.
- Dashboard de save actual.
- Inventory Pro.
- Quantity Editor.
- Backup Browser.
- Verificacion y recalculo de checksum.

### Advertencias

- Usar bajo tu propio riesgo.
- Mantener backups manuales.
- No editar saves con el juego abierto.
- No subir saves personales al reporte de bugs.

## Artefactos

Adjuntar en GitHub Release:

```text
dist\EldenRingSaveManager.exe
```
