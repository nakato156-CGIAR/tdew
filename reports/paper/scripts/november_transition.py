"""Date the dry-to-wet transition in the region where the exceedances occur.

The manuscript attributes the November concentration of extreme values to the dry-to-wet
transition, and until now that attribution rested on the regional literature rather than on
anything measured here. Gridded precipitation over the identical domain and period settles
it directly.

Precipitation is on a coarser grid than the dew-point field, which is immaterial for a
regional monthly climatology: each dew-point cell is matched to its nearest precipitation
cell, and the question asked of the result is only which month the rains arrive in.

Writes figures/S5_november_transition.png and prints the monthly climatology.
"""
import os
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

RES = os.environ.get("RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")
PREC = os.environ.get("PREC_NC", "/media/ppalacios/Data1/henry_simcast_peru/prec/data.nc")
HOT_CACHE = os.environ.get("HOT_IDS_CACHE",
                           str(Path(__file__).resolve().parent / ".exceedance_cells.pkl"))
OUT = Path(__file__).resolve().parent.parent / "figures"
MONTHS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
WARM = 35.0


def _hot_of(f):
    d = pd.read_parquet(f, columns=["ID", "TD_predicted"])
    return d.loc[d["TD_predicted"] > WARM, "ID"].unique()


def exceedance_cells() -> np.ndarray:
    """Cells carrying any reconstructed value above the threshold.

    Cached next to this script rather than in a temp directory: a reboot wiped the
    scratchpad copy once already, and rebuilding it is a full scan of the field.
    """
    p = Path(HOT_CACHE)
    if p.exists():
        return pickle.load(open(p, "rb"))
    import glob
    from concurrent.futures import ProcessPoolExecutor
    fs = sorted(glob.glob(f"{RES}/tuning/predictions_2017_2020/id_bucket=*/pred.parquet"))
    print(f"building exceedance-cell list from {len(fs)} buckets ...")
    with ProcessPoolExecutor(12) as ex:
        parts = [a for a in ex.map(_hot_of, fs, chunksize=32) if len(a)]
    ids = np.unique(np.concatenate(parts))
    pickle.dump(ids, open(p, "wb"))
    return ids


def main() -> int:
    zt = pd.read_parquet(f"{RES}/zone_table.parquet")
    sd = pd.read_parquet(f"{RES}/tuning/support_distance.parquet", columns=["ID", "tier"])
    zt = zt.merge(sd, on="ID", how="inner")

    hot = set(exceedance_cells().tolist())
    print(f"cells with any value above {WARM:.0f} C: {len(hot):,}")

    groups = {
        "affected cells": zt[zt["ID"].isin(hot)],
        "same class, within domain": zt[(zt.zone_id == 0) & (zt.tier == "within")],
        "whole released field": zt,
    }

    ds = xr.open_dataset(PREC)
    prec = ds["Prec"]
    lat = prec["Y"].values
    lon = prec["X"].values
    month = pd.to_datetime(prec["T"].values).month

    print(f"precipitation: {prec.shape}, {pd.to_datetime(prec['T'].values[0]).date()} "
          f"to {pd.to_datetime(prec['T'].values[-1]).date()}\n")

    curves = {}
    for name, g in groups.items():
        iy = np.clip(np.searchsorted(lat, g.lat.to_numpy()), 0, lat.size - 1)
        ix = np.clip(np.searchsorted(lon, g.lon.to_numpy()), 0, lon.size - 1)
        # unique precipitation cells covering this group, weighted by how many dew-point
        # cells fall in each
        pairs, counts = np.unique(np.c_[iy, ix], axis=0, return_counts=True)
        w = counts / counts.sum()
        series = prec.values[:, pairs[:, 0], pairs[:, 1]]          # time x cells
        regional = np.nansum(series * w[None, :], axis=1)           # mm/day, area-weighted
        monthly = np.array([np.nanmean(regional[month == m + 1]) for m in range(12)])
        curves[name] = monthly
        onset = int(np.argmax(np.diff(np.r_[monthly[-1], monthly]))) + 1
        print(f"{name:>28}  {'  '.join(f'{v:5.1f}' for v in monthly)}")
        print(f"{'':>28}  steepest monthly increase into month {onset} "
              f"({MONTHS[onset - 1]}), +{np.max(np.diff(np.r_[monthly[-1], monthly])):.2f} mm/day\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax, bx) = plt.subplots(1, 2, figsize=(11, 4.2))
    x = np.arange(1, 13)
    colours = {"affected cells": "#c0392b", "same class, within domain": "#2980b9",
               "whole released field": "#7f8c8d"}
    for name, y in curves.items():
        ax.plot(x, y, "o-", label=name, color=colours[name], lw=1.8, ms=4)
        bx.bar(x + (0.26 * (list(curves).index(name) - 1)),
               np.diff(np.r_[y[-1], y]), width=0.25, label=name, color=colours[name])
    for a in (ax, bx):
        a.set_xticks(x)
        a.set_xticklabels(MONTHS)
        a.axvspan(10.5, 11.5, color="#f1c40f", alpha=0.25, zorder=0)
        a.grid(alpha=0.25, axis="y")
    ax.set_ylabel("mean precipitation (mm/day)")
    ax.set_title("Monthly precipitation climatology, 1981–2016", fontsize=10)
    ax.legend(fontsize=8, frameon=False)
    bx.axhline(0, color="k", lw=1)
    bx.set_ylabel("change from previous month (mm/day)")
    bx.set_title("Month-on-month change; November shaded", fontsize=10)
    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "S5_november_transition.png", dpi=150)
    plt.close(fig)
    print(f"wrote {OUT / 'S5_november_transition.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
