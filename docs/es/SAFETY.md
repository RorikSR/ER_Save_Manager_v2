# Seguridad, Backups Y Checksum

## Regla Principal

No edites saves mientras Elden Ring esta abierto.

## Backups Automaticos

Las operaciones de escritura usan backups automaticos en:

```text
data/backups/
```

Tambien hay herramientas legacy que pueden usar:

```text
data/archive/
data/backup/
```

Estas carpetas son datos locales y no deben subirse a GitHub.

## Checksum

El proyecto recalcula y valida checksums MD5 internos del save.

La rutina principal vive en:

```text
logic/checksum.py
```

Prueba recomendada:

```powershell
python tools\test_checksum.py
```

Resultado esperado:

- `before_valid: True`
- `after_once_valid: True`
- `after_twice_valid: True`
- `idempotent: True`

## Rollback Manual

Si algo sale mal:

1. Cierra la app.
2. Abre `data/backups/`.
3. Copia el backup correcto.
4. Reemplaza el `ER0000.sl2` o `ER0000.co2` en la carpeta del juego.
5. Abre la app y usa `Verify current save`.

## Online / Anti-Cheat

Usar saves modificados online puede tener riesgos. La recomendacion segura es:

- Editar offline.
- Mantener backups limpios.
- No usar objetos imposibles o cantidades absurdas.
- No mezclar saves modificados con sesiones online si no entiendes las consecuencias.
