# (tr)uSDX · Riel de batería modular — BricoHams

Integración compacta y modular para el transceptor QRP **(tr)uSDX**:

- **Carcasa** del equipo: *Housing for (tr)uSDX* de **DL2MAN** (sin cambios).
- **Batería** 3×18650: *battery-slider* de DL2MAN + *Battery Lead Cover* de **KD9WNR** (sin cambios).
- **Base**: *(tr)uSDX Stand with ATU-10 Enclosure* de **KD9WNR**, **modificada por BricoHams** con un **riel de cola de milano** en la trasera.

El riel usa **exactamente el mismo perfil de cola de milano que la tapa inferior con batería de DL2MAN**
(`bottom_cover_battery.stl`), con sus detents de clic. El mismo módulo de batería se monta:

| Dónde | Pieza que lo recibe |
|---|---|
| Directamente en la radio | `bottom_cover_battery.stl` (DL2MAN, original) |
| En la base / soporte | `trusdx-stand_battery-rail_BricoHams.stl` (este repo) |
| En un soporte ya impreso | `rail-adapter_glue-on_BricoHams.stl` (este repo, se pega) |

Cambias la batería de la radio a la base (o viceversa) en segundos, sin herramientas.

![Montaje](images/assembly_left.png)

## Piezas a imprimir

| STL | Origen | Notas |
|---|---|---|
| `stl/trusdx-stand_battery-rail_BricoHams.stl` | **Nuevo** (remix KD9WNR) | Soporte con riel, tope y marca de agua |
| `stl/rail-adapter_glue-on_BricoHams.stl` | **Nuevo** | Opcional: riel suelto para pegar a un soporte ya impreso |
| `battery-slider.stl` *o* `battery-slider-witchusbcharger_dl1mad.stl` | DL2MAN / DL1MAD | Portapilas deslizante (descargar del original) |
| `trusdx-battery-lead-shroud.stl` | KD9WNR | Protector de los cables del portapilas |
| `stand-cover.stl`, `atu-10-enclosure.stl` | KD9WNR | Sin cambios |
| Carcasa completa | DL2MAN | Sin cambios |

`stl/_assembly_preview_DO-NOT-PRINT.stl` es solo para ver el conjunto montado.

## Documentación

1. [Proceso de diseño y medidas](docs/01_proceso_diseno.md)
2. [Impresión](docs/02_impresion.md)
3. [Montaje y cableado](docs/03_montaje.md)
4. [Atribución y licencias](ATTRIBUTION.md)

## Regenerar las piezas

```bash
pip install -r requirements.txt
python src/build.py --call EA4XXX     # tu indicativo en la marca de agua (opcional)
python src/render_previews.py         # imágenes de images/
```

Los parámetros (holguras, altura del tope, grosor…) están al principio de `src/build.py`.

## Licencia

Las piezas nuevas y modificadas: **CC BY-NC-SA 4.0** — ver [LICENSE.md](LICENSE.md).
Las piezas originales mantienen la licencia de sus autores — ver [ATTRIBUTION.md](ATTRIBUTION.md).

---
**BricoHams** · hecho por radioaficionados, para radioaficionados.
