"""Build the supplementary zone table and map.

The 41 mapped units of the SENAMHI classification are the unit of model selection, and the
FAO-56 table reports results by moisture class, so the reader needs to know what the classes
are and where they lie.

SENAMHI defines 38 climate types (37 Thornthwaite symbols plus a glacier class). The published
shapefile carries three further units that are not climate types -- two lakes and the coastal
lomas -- which is why 41 units appear here. The 37 Thornthwaite symbols in the shapefile match
the official list in CUADRO 3.1 of "Climas del Peru" (SENAMHI 2021) exactly.

Cell counts are taken over the *released field* (cells where the gridded dew point exists),
not over the full rectangular grid. The grid is a complete 1,422 x 1,982 rectangle and so
includes ocean; counting over it inflates the coastal zones. Dew-point coverage is the
land mask here, being exactly the domain the product covers.

Writes figures/S4_zone_map.png and a markdown table on stdout.
"""
import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from geo_overlay import add_peru_outline

RES = os.environ.get("RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")
OUT = Path(__file__).resolve().parent.parent / "figures"
CACHE = os.environ.get("PRODUCT_IDS_CACHE", "")

# Standard Thornthwaite letters. The first letter is the moisture index and the primed
# letter the thermal efficiency; both are read directly from the zone label. The
# parenthetical seasonal code follows SENAMHI's own legend and is left verbatim.
MOISTURE = {"A": "perhumid", "B": "humid", "C": "subhumid", "D": "semi-arid", "E": "arid"}
THERMAL = {"A'": "megathermal", "B'": "mesothermal", "C'": "microthermal",
           "D'": "tundra", "E'": "frost"}


def fix_mojibake(label: str) -> str:
    """Repair labels read from the .dbf as Latin-1 when they are in fact UTF-8.

    "Lago Junin" arrives with its accent mangled and would otherwise be published so.
    """
    try:
        return label.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return label


def product_ids() -> np.ndarray:
    """IDs of the released field (cells carrying a reconstruction)."""
    if CACHE and Path(CACHE).exists():
        return pickle.load(open(CACHE, "rb"))
    import glob
    from concurrent.futures import ProcessPoolExecutor
    fs = sorted(glob.glob(f"{RES}/tuning/predictions_2017_2020/id_bucket=*/pred.parquet"))
    with ProcessPoolExecutor(12) as ex:
        parts = list(ex.map(_ids_of, fs, chunksize=32))
    return np.unique(np.concatenate(parts))


def _ids_of(f):
    return pd.read_parquet(f, columns=["ID"])["ID"].unique()


def decode(label: str):
    """Split a zone label into (moisture, seasonal code, thermal), or None for landforms."""
    lab = label.strip()
    if lab[0] not in MOISTURE:
        return None
    moisture = MOISTURE[lab[0]]
    seasonal = lab[lab.find("(") + 1:lab.find(")")].strip() if "(" in lab else ""
    tail = lab[lab.rfind(")") + 1:].strip() if ")" in lab else ""
    return moisture, seasonal, THERMAL.get(tail, tail)


def main() -> int:
    zt = pd.read_parquet(f"{RES}/zone_table.parquet")
    ids = set(product_ids().tolist())
    masked = zt[zt["ID"].isin(ids)].copy()
    print(f"full grid {len(zt):,} cells; released field {len(masked):,} "
          f"({100 * len(masked) / len(zt):.1f}%)\n")

    # ---------------------------------------------------------------- table
    masked["zone_label"] = masked["zone_label"].map(fix_mojibake)
    g = (masked.groupby(["zone_id", "zone_label"])["ID"].size()
         .reset_index(name="cells").sort_values("zone_id"))
    full = zt.groupby("zone_id")["ID"].size()
    rows = []
    for _, r in g.iterrows():
        d = decode(r.zone_label)
        moisture, seasonal, thermal = d if d else ("--", "--", "--")
        rows.append({
            "zone": int(r.zone_id), "label": r.zone_label,
            "moisture": moisture, "seasonal": seasonal, "thermal": thermal,
            "cells": int(r.cells),
            "pct": 100 * r.cells / len(masked),
            "grid_cells": int(full.loc[r.zone_id]),
        })
    t = pd.DataFrame(rows)

    print("| Zone | Label | Moisture | Seasonal | Thermal | Cells | % of field |")
    print("|---:|:---|:---|:---:|:---|---:|---:|")
    for _, r in t.iterrows():
        print(f"| {r.zone} | `{r.label}` | {r.moisture} | {r.seasonal or '--'} | "
              f"{r.thermal} | {r.cells:,} | {r.pct:.2f} |")

    inflated = t[t.grid_cells > 1.5 * t.cells]
    print(f"\nzones whose full-grid count overstates the field by >50% "
          f"(i.e. mostly ocean): {len(inflated)}")
    for _, r in inflated.sort_values("grid_cells", ascending=False).head(6).iterrows():
        print(f"   zone {r.zone:>2} `{r.label:<14}` field {r.cells:>8,} vs grid {r.grid_cells:>8,}")

    t.to_csv(OUT.parent / "scripts" / "zone_table_supplement.csv", index=False)

    # ---------------------------------------------------------------- map
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap, BoundaryNorm
    from matplotlib.patches import Patch

    lons = np.sort(zt.lon.unique())
    lats = np.sort(zt.lat.unique())
    ix = np.searchsorted(lons, masked.lon.to_numpy())
    iy = np.searchsorted(lats, masked.lat.to_numpy())
    grid = np.full((lats.size, lons.size), np.nan)
    grid[iy, ix] = masked.zone_id.to_numpy()

    # Colour by moisture class so the map reads as a wet-to-dry gradient; the four
    # landform classes get greys so they do not masquerade as climate types.
    families = {"A": "Blues", "B": "YlGnBu", "C": "YlGn", "D": "YlOrBr", "E": "OrRd"}
    labels = {z: fix_mojibake(l) for z, l in
              zt.drop_duplicates("zone_id").set_index("zone_id")["zone_label"].items()}
    colours = {}
    for letter, cmap_name in families.items():
        zs = sorted(z for z, l in labels.items() if l.strip().startswith(letter))
        cm = plt.get_cmap(cmap_name)
        for k, z in enumerate(zs):
            colours[z] = cm(0.30 + 0.62 * (k / max(len(zs) - 1, 1)))
    greys = plt.get_cmap("Greys")
    others = sorted(z for z in labels if z not in colours)
    for k, z in enumerate(others):
        colours[z] = greys(0.35 + 0.45 * (k / max(len(others) - 1, 1)))

    order = sorted(labels)
    cmap = ListedColormap([colours[z] for z in order])
    norm = BoundaryNorm([z - 0.5 for z in order] + [order[-1] + 0.5], cmap.N)

    fig, (ax, lax) = plt.subplots(
        1, 2, figsize=(13.5, 9), gridspec_kw={"width_ratios": [1.0, 0.92]})
    ax.imshow(grid, origin="lower", cmap=cmap, norm=norm, interpolation="nearest",
              extent=[lons.min(), lons.max(), lats.min(), lats.max()])
    ax.set_xlabel("longitude (°E)")
    ax.set_ylabel("latitude (°N)")
    ax.set_title("SENAMHI Thornthwaite zones over the released field", fontsize=11)
    ax.set_aspect("equal")
    add_peru_outline(ax)

    cnt = t.set_index("zone")["cells"].to_dict()
    handles = [Patch(facecolor=colours[z],
                     label=f"{z:>2}  {labels[z]:<14} {cnt.get(z, 0):>8,}")
               for z in order]
    lax.axis("off")
    lax.legend(handles=handles, loc="center left", ncol=2, frameon=False,
               prop={"family": "monospace", "size": 7.4}, handlelength=1.1,
               labelspacing=0.34, title="zone  label            cells",
               title_fontproperties={"family": "monospace", "size": 8, "weight": "bold"})
    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "S4_zone_map.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nwrote {OUT / 'S4_zone_map.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
