#!/usr/bin/env python3
"""Genera las imágenes de images/ (vista previa rápida con matplotlib)."""
import pathlib, numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT = pathlib.Path(__file__).resolve().parents[1]
S, I = ROOT / "stl", ROOT / "images"

def shot(ms, cols, el, az, out, title, zoom=1.0, center=None):
    fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(projection="3d")
    allb = np.vstack([m.bounds for m in ms]); lo, hi = allb.min(0), allb.max(0)
    c = (lo+hi)/2 if center is None else np.array(center); r = (hi-lo).max()/2/zoom
    # luz que sigue a la cámara
    e, a = np.radians(el), np.radians(az)
    cam = np.array([np.cos(e)*np.cos(a), np.cos(e)*np.sin(a), np.sin(e)])
    L = cam + np.array([0, 0, 0.6]); L /= np.linalg.norm(L)
    for m, col in zip(ms, cols):
        mm = m if len(m.faces) < 60000 else m.simplify_quadric_decimation(face_count=60000)
        sh = np.clip(mm.face_normals @ L, 0, 1)*0.7 + 0.3
        ax.add_collection3d(Poly3DCollection(mm.triangles, facecolors=np.clip(sh[:, None]*np.array(matplotlib.colors.to_rgb(col)), 0, 1), edgecolor="none"))
    for k, s in enumerate("xyz"): getattr(ax, f"set_{s}lim")(c[k]-r, c[k]+r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(el, az); ax.set_axis_off(); ax.set_title(title)
    fig.text(0.98, 0.02, "BricoHams", ha="right", alpha=0.35, fontsize=14, fontweight="bold")
    plt.tight_layout(); plt.savefig(out, dpi=90); plt.close()

if __name__ == "__main__":
    st = trimesh.load(S / "trusdx-stand_battery-rail_BricoHams.stl")
    sl = trimesh.load(ROOT / "vendor" / "battery-slider.stl"); sl.apply_translation([6-45, 73.8, 28])
    G, O = "#b8bcc2", "#f0a020"
    shot([st, sl], [G, O], 25, 35, I/"assembly_back.png", "Soporte KD9WNR + riel + battery-slider DL2MAN")
    shot([st], [G], 25, 55, I/"stand_rail_back.png", "Riel cola de milano (estándar DL2MAN)")
    shot([st], [G], 10, 70, I/"rail_detail.png", "Detalle: ranura, tope inferior y marca", zoom=1.7, center=[6, 74, 55])
    shot([st], [G], 10, 195, I/"stand_side_watermark.png", "Marca de agua lateral")
    shot([trimesh.load(S/"rail-adapter_glue-on_BricoHams.stl")], ["#5b9bd5"], 60, -70, I/"adapter.png", "Adaptador para pegar")
