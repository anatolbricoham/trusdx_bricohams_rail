#!/usr/bin/env python3
"""
BricoHams - (tr)uSDX battery rail integration
Genera las piezas imprimibles a partir de los STL originales (carpeta vendor/).

Uso:
    pip install manifold3d trimesh numpy matplotlib
    python src/build.py                      # sin indicativo
    python src/build.py --call EA4XXX        # con indicativo en la marca de agua

Todas las medidas en mm. Ejes del soporte KD9WNR: X ancho, Y fondo (trasera en +Y), Z alto.
"""
import argparse, pathlib, numpy as np, trimesh, manifold3d as mf
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

ROOT = pathlib.Path(__file__).resolve().parents[1]
VENDOR, OUT = ROOT / "vendor", ROOT / "stl"

# ---------------- Estándar de cola de milano DL2MAN (medido de bottom_cover_battery.stl) ----------
DT_NECK   = 27.2   # ancho de la ranura en la boca (cara exterior)
DT_BASE   = 29.2   # ancho de la ranura en el fondo
DT_DEPTH  = 3.0    # profundidad de la ranura
DT_EXTRA  = 0.0    # holgura extra por lado (+0.1/+0.2 si tu impresora aprieta)
DIMPLE_Z  = (10.0, 50.0)  # posición de los detents a lo largo del slider (desde su extremo)
DIMPLE_D, DIMPLE_DEPTH = 2.6, 0.6
SLIDER_LEN = 60.0  # largo del battery-slider DL2MAN en dirección de deslizamiento

# ---------------- Integración en el soporte KD9WNR (trusdx-stand.stl) ---------------------------
BACK_Y   = 68.8    # cara trasera del soporte
CX       = 6.0     # centro en X del soporte (-40..52)
PAD_W    = 70.0    # ancho de la placa-riel
PAD_T    = 5.0     # grosor de la placa-riel (igual que bottom_cover_battery)
OVERLAP  = 0.2     # solape con la pared para que se fusionen
Z_STOP   = 28.0    # cota del tope inferior: el slider ocupa Z_STOP..Z_STOP+60
STOP_T   = 4.0     # grosor del tope inferior
Z_TOP    = 90.0    # altura del soporte (la ranura queda abierta por arriba)
CHAMFER  = 0.6     # chaflán de entrada de la ranura

# ---------------- Marca de agua ------------------------------------------------------------------
WM_TEXT, WM_DEPTH = "BRICOHAMS", 0.6

def to_mf(tm):
    return mf.Manifold(mf.Mesh(vert_properties=np.asarray(tm.vertices, np.float32),
                               tri_verts=np.asarray(tm.faces, np.uint32)))

def to_tm(m):
    g = m.to_mesh(); return trimesh.Trimesh(g.vert_properties[:, :3], g.tri_verts)

def box(x0, x1, y0, y1, z0, z1):
    return mf.Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0, y0, z0])

def text2d(txt, h):
    """Texto -> CrossSection en el plano XY (altura de mayúsculas ~h)."""
    tp = TextPath((0, 0), txt, size=h*1.38, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    polys = [p for p in tp.to_polygons() if len(p) > 2]
    cs = mf.CrossSection(polys, mf.FillRule.EvenOdd)
    b = cs.bounds()  # (xmin,ymin,xmax,ymax)
    return cs.translate([-(b[0]+b[2])/2, -(b[1]+b[3])/2])

def engrave_text(txt, h, depth):
    """Sólido de texto centrado en el origen, extruido en +Z de 0 a depth."""
    return mf.Manifold.extrude(text2d(txt, h), depth)

def dovetail_groove(y_face, z0, z1, extra=DT_EXTRA):
    """Ranura hembra abierta hacia +Y en y_face, que entra en -Y. Va de z0 a z1 (eje Z)."""
    n, b = DT_NECK/2 + extra, DT_BASE/2 + extra
    yb = y_face - DT_DEPTH - extra
    pts = [(CX-n, y_face+0.01), (CX+n, y_face+0.01), (CX+b, yb), (CX-b, yb)]
    cs = mf.CrossSection([pts[::-1]])  # sentido antihorario
    g = mf.Manifold.extrude(cs, z1-z0).translate([0, 0, z0])
    # chaflán de entrada en la boca superior
    c = CHAMFER
    ent = mf.Manifold.extrude(mf.CrossSection([[(CX-n, y_face-c), (CX+n, y_face-c), (CX+n+c, y_face+0.01), (CX-n-c, y_face+0.01)]]), z1-z0).translate([0, 0, z0])
    return g + ent

def dimples(y_floor):
    s = mf.Manifold.sphere(DIMPLE_D/2, 32)
    r = DIMPLE_D/2
    return mf.Manifold.batch_boolean([s.translate([CX, y_floor - DIMPLE_DEPTH + r, Z_STOP+z]) for z in DIMPLE_Z],
                                     mf.OpType.Add)

def rail_pad(call=None, y_back=BACK_Y, with_wedge=True):
    """Placa con ranura DL2MAN, tope inferior, detents y marca de agua grabada."""
    y_face = y_back + PAD_T
    pad = box(CX-PAD_W/2, CX+PAD_W/2, y_back-OVERLAP, y_face, Z_STOP-STOP_T, Z_TOP)
    # cuña a 45° bajo la placa: se imprime sin soportes en el soporte (riel vertical)
    z0 = Z_STOP - STOP_T
    wedge = mf.Manifold.extrude(mf.CrossSection([[(y_back-OVERLAP, z0), (y_back-OVERLAP, z0-PAD_T-OVERLAP), (y_face, z0)]][::1]), PAD_W)
    wedge = wedge.transform([[0, 0, 1, CX-PAD_W/2], [1, 0, 0, 0], [0, 1, 0, 0]])
    if wedge.volume() == 0:  # por si el sentido del polígono queda invertido
        wedge = mf.Manifold.extrude(mf.CrossSection([[(y_face, z0), (y_back-OVERLAP, z0-PAD_T-OVERLAP), (y_back-OVERLAP, z0)]]), PAD_W)
        wedge = wedge.transform([[0, 0, 1, CX-PAD_W/2], [1, 0, 0, 0], [0, 1, 0, 0]])
    if with_wedge:
        pad += wedge
    pad -= dovetail_groove(y_face, Z_STOP, Z_TOP+1)
    pad -= dimples(y_face - DT_DEPTH)
    # marca de agua en las bandas laterales (texto vertical), visible al retirar la batería
    side = (DT_BASE/2 + PAD_W/2) / 2
    for i, t in enumerate([WM_TEXT, call or "(tr)uSDX"]):
        txt = engrave_text(t, 6.0, WM_DEPTH + 0.02)
        # texto XY -> plano XZ de la cara del riel, leyendo de abajo arriba, grabado hacia -Y
        txt = txt.transform([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0]])
        x = CX - side if i == 0 else CX + side
        pad -= txt.translate([x, y_face - WM_DEPTH, (Z_STOP + Z_TOP) / 2])
    return pad

def side_watermark(call=None):
    """Texto grabado en la pared lateral izquierda exterior (x=-40) del soporte."""
    t = WM_TEXT + (f"  {call}" if call else "")
    txt = engrave_text(t, 5.0, WM_DEPTH + 0.02)
    # texto XY -> plano YZ de la cara exterior x=-40, legible desde fuera, grabado hacia +X
    txt = txt.transform([[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0]])
    return txt.translate([-40 + WM_DEPTH, 40, 16])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--call", default=None, help="indicativo, p.ej. EA4XXX")
    a = ap.parse_args(); call = a.call.upper() if a.call else None
    OUT.mkdir(exist_ok=True)
    stand = to_mf(trimesh.load(VENDOR / "trusdx-stand.stl"))
    pad = rail_pad(call)

    # 1) Soporte KD9WNR con riel integrado + marca de agua lateral
    stand_rail = (stand + pad) - side_watermark(call)
    to_tm(stand_rail).export(OUT / "trusdx-stand_battery-rail_BricoHams.stl")

    # 2) Adaptador independiente (para soportes ya impresos): se pega con CA/epoxi a la trasera
    adapter = rail_pad(call, y_back=0.0 + OVERLAP, with_wedge=False)        # cara de pegado en y=0
    adapter = adapter.translate([-CX, 0, -(Z_STOP-STOP_T)])
    adapter = adapter.rotate([90, 0, 0])                   # imprimir con la cara de pegado en la cama
    tm = to_tm(adapter); tm.apply_translation(-tm.bounds[0] * [1, 1, 1])
    tm.export(OUT / "rail-adapter_glue-on_BricoHams.stl")

    # 3) Ensamblado de referencia (no imprimir): soporte + slider DL2MAN en posición
    sl = trimesh.load(VENDOR / "battery-slider.stl")
    sl.apply_translation([CX - 45.0, BACK_Y + PAD_T, Z_STOP])
    asm = trimesh.util.concatenate([to_tm(stand_rail), sl])
    asm.export(OUT / "_assembly_preview_DO-NOT-PRINT.stl")
    for f in sorted(OUT.glob("*.stl")):
        t = trimesh.load(f); print(f"{f.name:48s} {t.extents.round(1)}  watertight={t.is_watertight}")

if __name__ == "__main__":
    main()
