# 1 · Proceso de diseño

## Objetivo

Integrar la batería 3×18650 en la base del (tr)uSDX de forma **compacta**, **modular** (quitar y poner sin herramientas) y **compatible** con las piezas ya existentes en la comunidad.

## Análisis de las piezas originales

Todas las medidas se tomaron directamente de los STL publicados (secciones con `trimesh`).

### Carcasa DL2MAN

- Caja de 90 × 60 × 30 mm.
- `bottom_cover_battery.stl` es una tapa de 90 × 60 × 5 mm con una **ranura de cola de milano** a lo largo de los 60 mm.
- `battery-slider.stl` es un perfil en U de 90 × 29,5 × 60 mm para un portapilas 3×18650. Por detrás lleva la **lengüeta macho** que entra en esa ranura.

### Perfil de cola de milano (estándar DL2MAN)

| Elemento | Ranura (hembra, en la tapa) | Lengüeta (macho, en el slider) |
|---|---|---|
| Ancho en la boca | 27,2 mm | 25,2 mm (cuello) |
| Ancho en el fondo | 29,2 mm | 27,6 mm (punta) |
| Profundidad | 3,0 mm | 3,0 mm |
| Holgura lateral | — | aprox. 0,8–1,0 mm |
| Detents | 2 cavidades de 0,5 mm a 10 y 50 mm | 2 resaltes de 0,5 mm (Ø2 mm) a 10 y 50 mm |

Los resaltes de la lengüeta encajan en las cavidades de la ranura y producen el **clic** de retención.

### Soporte KD9WNR

- Cuña hueca de 92 × 59 × 90 mm (X: −40…52, Y: 9,8…68,8, Z: 0…90), abierta por abajo y cerrada con `stand-cover.stl`.
- La **cara trasera** es vertical y plana (y = 68,8) en toda su altura, con paredes de 3 mm.
- En la trasera hay una **ranura pasacables** en X −24…36 y Z 12,7…18,8.

## Decisiones de diseño

1. **Reutilizar el estándar DL2MAN** en vez de inventar un riel nuevo. Así el mismo slider sirve en la radio y en la base, y cualquier variante del slider (como la de DL1MAD con cargador USB-C) también encaja.
2. **Riel vertical en la trasera del soporte.** El slider entra desde arriba y apoya en un tope inferior, de modo que la gravedad también lo mantiene en su sitio. Es la cara más grande y plana, y no interfiere con la radio, la tapa inferior ni el ATU-10.
3. **Tope en Z = 28 mm.** La batería ocupa Z 28…88 y queda por encima de la ranura pasacables, que sigue libre para llevar los cables al compartimento interior.
4. **Placa-riel de 70 × 5 mm** (el mismo grosor que `bottom_cover_battery`). Se fusiona con la pared y añade solo 5 mm de fondo.
5. **Cuña de 45°** bajo la placa para imprimir sin soportes.
6. **Chaflán de entrada de 0,6 mm** en la boca de la ranura para que el slider entre suave.
7. **Marca de agua BricoHams:**
   - Grabada a 0,6 mm en la pared lateral izquierda, visible siempre.
   - En las bandas laterales del riel: BRICOHAMS y el indicativo (o "(tr)uSDX"), visibles al sacar la batería.

## Resultado

- El fondo total del conjunto es de unos 94 mm (soporte 59 + riel 5 + slider 29,5).
- Comprobación de interferencias con el slider original colocado, hecha con *booleanas* en `manifold3d`:
  - Asentado: 0,29 mm³, que es contacto coplanario sin interferencia real.
  - Desplazado 10 mm: unos 2,5 mm³. Es el resalte pasando por el fondo de la ranura, es decir, el clic.

## Parámetros (`src/build.py`)

| Parámetro | Valor | Uso |
|---|---|---|
| `DT_EXTRA` | 0,0 | Holgura extra por lado. Súbela a +0,1/+0,2 si el slider entra duro |
| `Z_STOP` | 28 | Altura del tope inferior |
| `PAD_W`, `PAD_T` | 70, 5 | Tamaño de la placa-riel |
| `DIMPLE_DEPTH` | 0,6 | Profundidad de los detents. Súbela para un clic más fuerte |
| `WM_TEXT` | BRICOHAMS | Texto de la marca de agua |
| `--call` | — | Indicativo en la banda derecha del riel y en el lateral |

## Herramientas

Python 3, `manifold3d` (booleanas robustas), `trimesh` (lectura y secciones de STL) y `matplotlib` (texto y vistas previas).
