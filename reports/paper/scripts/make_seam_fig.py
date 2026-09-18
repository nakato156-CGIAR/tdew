"""F3: seam artefact test, seasonality-free, with a natural-variability control.

An earlier version of this figure compared Jan-2017 (predicted) with Dec-2016 (observed).
Because those are DIFFERENT months it was dominated by the real Dec->Jan seasonal cycle and was a
weak artefact test. This version uses equal-length FULL-YEAR windows (so the seasonal cycle cancels)
and adds a model-free control:

  Panel A (reference): obs(2013-2016) - obs(2009-2012)   <- both OBSERVED, 4 yr vs 4 yr
  Panel B (seam test): pred(2017-2020) - obs(2013-2016)  <- the fill vs last observed window
  Panel C: distributions of A and B overlaid.

If B resembles A in magnitude and texture, the fill introduces no artefact beyond the
period-to-period variability the observed record itself shows.

Per-cell window means are cached to $RES/tuning/seam_windows_cache.parquet, so re-plotting is fast.
"""
import glob, os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from geo_overlay import add_peru_outline

FULL = "/media/ppalacios/Data1/henry_simcast_peru_full"
RES = f"{FULL}/results_tuning"
PRED = f"{RES}/tuning/predictions_2017_2020"
TRAIN = f"{RES}/bucketed_training_data"
GRID = f"{FULL}/td/Outputs/grid_index.parquet"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
CACHE = f"{RES}/tuning/seam_windows_cache.parquet"

W1 = range(2009, 2013)   # observed window 1
W2 = range(2013, 2017)   # observed window 2 (last observed)
# predicted window = 2017-2020 (all of pred.parquet)


def agg(bnum):
    tdir = Path(TRAIN) / f"id_bucket={bnum:04d}"
    pfile = Path(PRED) / f"id_bucket={bnum:04d}" / "pred.parquet"

    def win_mean(years, col="TD"):
        fr = [pd.read_parquet(tdir / f"train_{y}.parquet", columns=["ID", col])
              for y in years if (tdir / f"train_{y}.parquet").exists()]
        if not fr:
            return None
        return pd.concat(fr, ignore_index=True).groupby("ID")[col].mean()

    a, b = win_mean(W1), win_mean(W2)
    if not pfile.exists() or a is None or b is None:
        return None
    p = pd.read_parquet(pfile, columns=["ID", "TD_predicted"]).groupby("ID")["TD_predicted"].mean()
    df = pd.concat([a.rename("w1"), b.rename("w2"), p.rename("w3")], axis=1).dropna()
    return df.reset_index()


def main():
    if os.path.exists(CACHE):
        df = pd.read_parquet(CACHE)
        print(f"loaded cache: {len(df):,} cells", flush=True)
    else:
        nums = sorted(int(Path(p).name.split("=")[1]) for p in glob.glob(f"{PRED}/id_bucket=*"))
        print(f"buckets: {len(nums)}", flush=True)
        parts = []
        with ProcessPoolExecutor(max_workers=14) as ex:
            for r in ex.map(agg, nums, chunksize=16):
                if r is not None and len(r):
                    parts.append(r)
        df = pd.concat(parts, ignore_index=True)
        df.to_parquet(CACHE, index=False)
        print(f"cells with all three windows: {len(df):,} (cached)", flush=True)

    df["A"] = df["w2"] - df["w1"]      # obs - obs  (natural variability)
    df["B"] = df["w3"] - df["w2"]      # pred - obs (seam test)
    grid = pd.read_parquet(GRID)
    m = df.merge(grid, on="ID", how="left").dropna(subset=["lon", "lat"])
    sA, sB = m["A"], m["B"]

    print("\n=== national statistics (annual-mean Td, °C) ===")
    for lab, s in [("A  obs2013-16 - obs2009-12 ", sA), ("B  pred2017-20 - obs2013-16", sB)]:
        print(f"  {lab}: mean {s.mean():+.3f}  sd {s.std():.3f}  "
              f"p1 {s.quantile(.01):+.2f}  p99 {s.quantile(.99):+.2f}  "
              f"|d|>1: {100*(s.abs()>1).mean():.1f}%")
    lim = float(np.ceil(max(sA.abs().quantile(.99), sB.abs().quantile(.99)) * 2) / 2)
    print(f"  shared colour limit: ±{lim:.1f} °C", flush=True)

    fig = plt.figure(figsize=(16.5, 8.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.95], wspace=0.42)
    for i, (col, title) in enumerate([
            ("A", "A. Reference: natural variability\nobserved 2013–2016 − observed 2009–2012"),
            ("B", "B. Seam test: gap-filled vs observed\npredicted 2017–2020 − observed 2013–2016")]):
        ax = fig.add_subplot(gs[0, i])
        sc = ax.scatter(m.lon, m.lat, c=m[col], s=0.12, cmap="RdBu_r",
                        vmin=-lim, vmax=lim, linewidths=0)
        ax.set_aspect("equal"); add_peru_outline(ax); ax.set_title(title, fontsize=11)
        ax.set_xlabel("lon")
        if i == 0:
            ax.set_ylabel("lat")
        cb = fig.colorbar(sc, ax=ax, shrink=0.55, pad=0.02)
        cb.set_label("Δ annual-mean Td (°C)", fontsize=9)

    ax = fig.add_subplot(gs[0, 2])
    bins = np.linspace(-lim, lim, 90)
    ax.hist(sA, bins=bins, alpha=0.55, label=f"A obs−obs (sd {sA.std():.2f})", color="#4c72b0")
    ax.hist(sB, bins=bins, alpha=0.55, label=f"B pred−obs (sd {sB.std():.2f})", color="#c44e52")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("Δ annual-mean Td (°C)"); ax.set_ylabel("number of cells")
    ax.set_xlim(-0.9, 0.9)
    ax.set_title("C. Distributions\n(B comparable to A ⇒ no seam artifact)", fontsize=11)
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.suptitle("Seam artifact test on equal-length full-year windows (seasonality removed)",
                 fontsize=12.5)
    fig.subplots_adjust(left=0.055, right=0.98, top=0.88, bottom=0.09)
    out = f"{OUT}/F3_seam_artifact_test.png"
    fig.savefig(out, dpi=150); plt.close(fig)
    print("WROTE", out, flush=True)


if __name__ == "__main__":
    main()
