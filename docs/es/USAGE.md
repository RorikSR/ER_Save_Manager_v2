# Guia de Uso

## Antes De Empezar

1. Cierra Elden Ring.
2. Haz una copia manual de tus saves importantes.
3. Abre `EldenRingSaveManager.exe`.
4. Configura la carpeta del juego desde `Edit > Change Default Directory`.
5. Configura SteamID desde `Edit > Change Default SteamID`.

## Modo Vanilla Y Seamless Co-op

- Vanilla usa `ER0000.sl2`.
- Seamless Co-op usa `ER0000.co2`.
- Puedes cambiar el modo desde `File > Seamless Co-op Mode`.
- El dashboard muestra el modo activo.

## Crear Un Perfil

1. Escribe un nombre en `New profile name`.
2. Pulsa `Create profile from current save`.
3. El perfil aparece en `Saved Profiles`.

## Cargar Un Perfil

1. Selecciona un perfil en `Saved Profiles`.
2. Pulsa `Load selected profile`.
3. La app crea backup del save actual antes de sobrescribir.

## Verificar Save

Pulsa `Verify current save` para revisar:

- Extension actual.
- Tamano del archivo.
- Checksum.
- Slots detectados.
- Personajes encontrados.
- MD5 del archivo.

## Inventory Pro

`Inventory Pro` permite explorar el catalogo completo de items.

Puedes filtrar por:

- Nombre.
- Categoria.
- Fuente: Base Game, DLC o Custom.
- Goods ID.
- Raw ID.
- IDs internos.

Botones disponibles:

- `Copy Goods ID`: copia el Goods ID seleccionado.
- `Export catalog`: exporta el catalogo actual a JSON.
- `Scan current save`: genera reporte real del inventario.
- `Edit quantities`: abre el editor de cantidades.

## Quantity Editor

El `Quantity Editor` permite modificar la cantidad actual de objetos que ya existen en el inventario del personaje.

Flujo:

1. Selecciona personaje.
2. Busca el objeto.
3. Selecciona la fila del objeto.
4. Usa `+1`, `+10`, `-1`, `-10` o escribe una cantidad exacta.
5. Confirma el cambio.

La app:

- Escribe sobre el indice exacto del objeto seleccionado.
- Crea backup automatico.
- Recalcula checksum.
- Verifica checksum despues del cambio.

## Backup Browser

`Backup Browser` muestra backups creados por la app.

Puedes:

- Ver fecha, archivo y MD5.
- Restaurar un backup.
- Abrir la carpeta de backups.

Antes de restaurar, se crea un backup del save actual.

## Convertir .sl2 / .co2

Usa `Convert .sl2 / .co2` para convertir entre formato vanilla y Seamless Co-op.

La app:

- Pide archivo origen.
- Pide ruta destino.
- Si el destino existe, crea backup antes.
- Recalcula checksum.
- Verifica el resultado.
