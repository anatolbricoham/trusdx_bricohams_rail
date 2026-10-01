# 2 · Impresión

## Ajustes recomendados (PETG)

| Ajuste | Soporte con riel | Adaptador | Slider DL2MAN |
|---|---|---|---|
| Altura de capa | 0,2 mm | 0,15 mm | 0,15 mm (recomendación de DL2MAN) |
| Paredes | 4 | 4 | 3 |
| Relleno | 20–25 % | 40 % | 20–25 % |
| Soportes | **No** | **No** | Según el original |
| Orientación | Tal cual viene en el STL (base abierta sobre la cama, riel vertical) | Cara de pegado sobre la cama | Según el original |
| Brim | 3–5 mm si la cama no agarra bien | No | No |

Temperaturas orientativas de PETG: boquilla a 235–245 °C, cama a 75–80 °C y ventilador al 30–50 %.

## Notas

- **Prueba de ajuste:** antes de imprimir el soporte entero (unas 6 h), imprime el **adaptador**, que es pequeño y rápido. Comprueba con él cómo desliza el slider:
  - Si entra duro, sube `DT_EXTRA` a 0,1–0,2 y regenera.
  - Si queda flojo y el clic no se nota, sube `DIMPLE_DEPTH` a 0,8.
- La marca de agua está grabada a 0,6 mm. Con boquilla de 0,4 se lee bien. Si quieres resaltarla, rellena el grabado con pintura acrílica y retira el sobrante.
- Si el laminador avisa de errores de malla en el soporte, vienen del STL original de KD9WNR. PrusaSlicer y Orca los reparan solos (opción "Reparar").
- Para la Anycubic Kobra S1 con PETG: limpia la cama con jabón, usa un brim de 3 mm y una primera capa lenta (20–30 mm/s).
