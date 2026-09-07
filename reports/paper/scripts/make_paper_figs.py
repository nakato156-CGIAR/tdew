"""Build paper figures F1, F2 and F4 from the filled product and observed history.

Parallel aggregation over all buckets (read-only), then matplotlib figures into
reports/paper/figures/:
  F1_national_td_timeseries_seam.png  national monthly-mean Td 2010-2020 (obs -> pred)
  F2_meanTd_map_2017_2020.png         mean Td 2017-2020 map
  F4_warm_tail_panel.png              histogram + map of >35 C cells + monthly incidence

F3 is produced by make_seam_fig.py; F5 from warm_tail_diagnostics.py output.
"""
import glob, os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FULL = "/media/ppalacios/Data1/henry_simcast_peru_full"
RES = f"{FULL}/results_tuning"
PRED = f"{RES}/tuning/predictions_2017_2020"
TRAIN = f"{RES}/bucketed_training_data"
GRID = f"{FULL}/td/Outputs/grid_index.parquet"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(OUT, exist_ok=True)

BINS = np.arange(-20, 45.01, 0.5)
WARM = 35.0


def agg_pred(pf):
    df = pd.read_parquet(pf, columns=["ID", "FECHA", "TD_predicted"])
    d = pd.to_datetime(df["FECHA"]); ym = (d.dt.year * 100 + d.dt.month)
    v = df["TD_predicted"].to_numpy()
    g = df.groupby("ID")["TD_predicted"]
    per_id = pd.DataFrame({"ID": g.mean().index.astype(int),
                           "mean_td": g.mean().to_numpy(), "max_td": g.max().to_numpy()})
    jan = df[(d.dt.year == 2017) & (d.dt.month == 1)].groupby("ID")["TD_predicted"].mean()
    return dict(per_id=per_id, jan=jan.rename("jan17"),
                msum=pd.Series(v).groupby(ym).sum(), mcnt=pd.Series(v).groupby(ym).count(),
                gt=pd.Series((v > WARM).astype("int64")).groupby(ym).sum(),
                hist=np.histogram(v, bins=BINS)[0])


def agg_obs(td_dir):
    files = glob.glob(f"{td_dir}/*.parquet")
    df = pd.concat([pd.read_parquet(f, columns=["ID", "FECHA", "TD"]) for f in files],
                   ignore_index=True)
    d = pd.to_datetime(df["FECHA"])
    ym = (d.dt.year * 100 + d.dt.month).to_numpy()
    m = (d.dt.year >= 2010).to_numpy()
    v = df["TD"].to_numpy()
    s = pd.Series(v[m], index=ym[m])
    dec16 = df[(d.dt.year == 2016) & (d.dt.month == 12)].groupby("ID")["TD"].mean()
    return dict(msum=s.groupby(level=0).sum(), mcnt=s.groupby(level=0).count(),
                dec16=dec16.rename("dec16"))


def to_dt(idx):
    return pd.to_datetime([f"{int(k)//100}-{int(k)%100:02d}-01" for k in idx])


def main():
    pred_files = sorted(glob.glob(f"{PRED}/id_bucket=*/pred.parquet"))
    train_dirs = sorted(glob.glob(f"{TRAIN}/id_bucket=*"))
    print(f"pred={len(pred_files)} train={len(train_dirs)}", flush=True)

    per_id, jan = [], []
    hist = np.zeros(len(BINS) - 1, dtype=np.int64)
    p_msum = pd.Series(dtype=float); p_mcnt = pd.Series(dtype=float); p_gt = pd.Series(dtype=float)
    with ProcessPoolExecutor(max_workers=14) as ex:
        for r in ex.map(agg_pred, pred_files):
            per_id.append(r["per_id"]); jan.append(r["jan"]); hist += r["hist"]
            p_msum = p_msum.add(r["msum"], fill_value=0)
            p_mcnt = p_mcnt.add(r["mcnt"], fill_value=0)
            p_gt = p_gt.add(r["gt"], fill_value=0)
    per_id = pd.concat(per_id, ignore_index=True); jan = pd.concat(jan)
    print(f"per-ID cells={len(per_id):,}", flush=True)

    o_msum = pd.Series(dtype=float); o_mcnt = pd.Series(dtype=float); dec16 = []
    with ProcessPoolExecutor(max_workers=14) as ex:
        for r in ex.map(agg_obs, train_dirs):
            o_msum = o_msum.add(r["msum"], fill_value=0)
            o_mcnt = o_mcnt.add(r["mcnt"], fill_value=0)
            dec16.append(r["dec16"])
    dec16 = pd.concat(dec16)

    grid = pd.read_parquet(GRID)
    pred_mm, obs_mm = (p_msum / p_mcnt).sort_index(), (o_msum / o_mcnt).sort_index()

    # ---- F1: national monthly-mean Td, seam ----
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.plot(to_dt(obs_mm.index), obs_mm.values, "-", color="#1f77b4", lw=1.4,
            label="observed Td (PISCO v1.1, 1981–2016)")
    ax.plot(to_dt(pred_mm.index), pred_mm.values, "-", color="#d62728", lw=1.4,
            label="predicted Td (filled, 2017–2020)")
    ax.axvline(pd.Timestamp("2017-01-01"), color="k", ls="--", lw=0.8, alpha=0.6)
    ax.set_ylabel("national mean Td (°C)"); ax.set_xlabel("year")
    ax.set_title("National monthly-mean dew point: observed → gap-filled (seam continuity)")
    ax.legend(loc="lower left", fontsize=8); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(f"{OUT}/F1_national_td_timeseries_seam.png", dpi=150)
    plt.close(fig)

    # ---- F2: mean-Td map ----
    m = per_id.merge(grid, on="ID", how="left").dropna(subset=["lon", "lat"])
    fig, ax = plt.subplots(figsize=(6.8, 8))
    sc = ax.scatter(m.lon, m.lat, c=m.mean_td, s=0.15, cmap="viridis", vmin=0, vmax=26, linewidths=0)
    ax.set_aspect("equal"); ax.set_xlabel("lon"); ax.set_ylabel("lat")
    ax.set_title("Mean gap-filled Td, 2017–2020 (°C)")
    fig.colorbar(sc, ax=ax, shrink=0.6, label="Td (°C)")
    fig.tight_layout(); fig.savefig(f"{OUT}/F2_meanTd_map_2017_2020.png", dpi=150); plt.close(fig)

    # ---- F4: warm-tail panel ----
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))
    centers = (BINS[:-1] + BINS[1:]) / 2
    axs[0].bar(centers, hist, width=0.5, color="#4c72b0")
    axs[0].axvline(WARM, color="r", ls="--", lw=1); axs[0].set_yscale("log")
    axs[0].set_xlabel("Td (°C)"); axs[0].set_ylabel("count (log)")
    axs[0].set_title("Distribution of all predicted Td (warm tail >35 °C)")
    warm = per_id[per_id.max_td > WARM].merge(grid, on="ID", how="left").dropna(subset=["lon", "lat"])
    axs[1].scatter(grid.lon, grid.lat, s=0.05, color="0.85", linewidths=0)
    axs[1].scatter(warm.lon, warm.lat, c=warm.max_td, s=2, cmap="hot_r", vmin=35, vmax=42, linewidths=0)
    axs[1].set_aspect("equal"); axs[1].set_xlabel("lon"); axs[1].set_ylabel("lat")
    axs[1].set_title(f"Cells with max Td >35 °C (n={len(warm):,})")
    frac = (p_gt / p_mcnt * 100).sort_index()
    axs[2].plot(to_dt(frac.index), frac.values, "-o", ms=3, color="#c44e52")
    axs[2].set_ylabel("% cells >35 °C"); axs[2].set_xlabel("month")
    axs[2].set_title("Fraction of cells >35 °C by month"); axs[2].grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(f"{OUT}/F4_warm_tail_panel.png", dpi=150); plt.close(fig)

    print("FIGURES DONE ->", OUT)


if __name__ == "__main__":
    main()
