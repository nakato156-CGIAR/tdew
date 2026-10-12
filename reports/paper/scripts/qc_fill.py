"""National QC of the 2017-2020 gap-filled Td product.

Parallel scan of all prediction buckets: value ranges, NaN count, outlier tail fractions,
national monthly-mean series, and the 2016->2017 seam. Read-only.
Produces the numbers quoted in paper.qmd section "The gap-filled product".
"""
import os, glob
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd

RES = "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"
PRED = f"{RES}/tuning/predictions_2017_2020"
TRAIN = f"{RES}/bucketed_training_data"


def _bucket_num(p):
    return int(Path(p).parent.name.split("=")[1])


def stat_pred(pred_file):
    df = pd.read_parquet(pred_file, columns=["FECHA", "TD_predicted"])
    v = df["TD_predicted"].to_numpy()
    fin = np.isfinite(v)
    vf = v[fin]
    d = pd.to_datetime(df["FECHA"])
    ym = d.dt.year * 100 + d.dt.month
    return {
        "n": int(v.size), "nan": int((~fin).sum()),
        "min": float(vf.min()) if vf.size else np.nan,
        "max": float(vf.max()) if vf.size else np.nan,
        "sum": float(vf.sum()), "cnt": int(vf.size),
        "g30": int((vf > 30).sum()), "g32": int((vf > 32).sum()),
        "g35": int((vf > 35).sum()), "lm15": int((vf < -15).sum()),
        "msum": pd.Series(v).groupby(ym).sum(), "mcnt": pd.Series(v).groupby(ym).count(),
    }


def stat_obs(train_dir):
    """Observed Td monthly means from one bucket (a nationwide lattice sample)."""
    files = glob.glob(f"{train_dir}/*.parquet")
    df = pd.concat([pd.read_parquet(f, columns=["FECHA", "TD"]) for f in files], ignore_index=True)
    d = pd.to_datetime(df["FECHA"])
    ym = (d.dt.year * 100 + d.dt.month).to_numpy()
    m = (d.dt.year >= 2013).to_numpy()
    v = df["TD"].to_numpy()
    s = pd.Series(v[m], index=ym[m])
    return s.groupby(level=0).sum(), s.groupby(level=0).count()


def main():
    pred_files = sorted(glob.glob(f"{PRED}/id_bucket=*/pred.parquet"), key=_bucket_num)
    train_dirs = sorted(glob.glob(f"{TRAIN}/id_bucket=*"))
    print(f"pred buckets: {len(pred_files)} | train dirs: {len(train_dirs)}")

    tot = {k: 0 for k in ["n", "nan", "cnt", "g30", "g32", "g35", "lm15"]}
    gmin, gmax, gsum = np.inf, -np.inf, 0.0
    msum = pd.Series(dtype=float); mcnt = pd.Series(dtype=float)
    with ProcessPoolExecutor(max_workers=14) as ex:
        for r in ex.map(stat_pred, pred_files):
            for k in tot:
                tot[k] += r[k]
            gmin = min(gmin, r["min"]); gmax = max(gmax, r["max"]); gsum += r["sum"]
            msum = msum.add(r["msum"], fill_value=0); mcnt = mcnt.add(r["mcnt"], fill_value=0)

    mean = gsum / tot["cnt"]
    print("\n=== national Td ranges (2017-2020 filled) ===")
    print(f"rows={tot['n']:,}  finite={tot['cnt']:,}  NaN={tot['nan']:,}")
    print(f"min={gmin:.2f}  mean={mean:.2f}  max={gmax:.2f} C")
    print("\n=== outlier tail (fraction of finite) ===")
    for k, lab in [("g30", ">30C"), ("g32", ">32C"), ("g35", ">35C"), ("lm15", "<-15C")]:
        print(f"  {lab:>6}: {tot[k]:,}  ({100*tot[k]/tot['cnt']:.4f}%)")

    osum, ocnt = stat_obs(train_dirs[0])
    pred_mm, obs_mm = msum / mcnt, osum / ocnt
    print("\n=== national monthly-mean Td: seam 2016->2017 ===")
    for ym in [201609, 201610, 201611, 201612, 201701, 201702, 201703]:
        src = "obs" if ym < 201700 else "pred"
        val = (obs_mm if ym < 201700 else pred_mm).get(ym, np.nan)
        print(f"  {ym} [{src}]: {val:.2f} C")
    print("\n=== pred annual-mean Td by year ===")
    for y in [2017, 2018, 2019, 2020]:
        yk = [k for k in pred_mm.index if k // 100 == y]
        print(f"  {y}: {np.mean([pred_mm[k] for k in yk]):.2f} C")
    print("\nQC DONE")


if __name__ == "__main__":
    main()
