"""Evaluate a bound on the dew-point excess over same-day minimum temperature.

Capping at Td <= Tmin is not viable: most reconstructed values, and the observed gridded
Td itself, exceed same-day Tmin. This evaluates the family Td <= Tmin + k, reporting for
each k how much of the field is altered, by how much, and what share of the >35 C
exceedances is removed.
"""
import glob
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd

RES = "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"
PRED = f"{RES}/tuning/predictions_2017_2020"
FTMIN = f"{RES}/future_tmin_by_bucket"
KS = [4, 5, 6, 8, 10, 12, 15]
WARM = 35.0


def one(b):
    pf = Path(PRED) / f"id_bucket={b:04d}" / "pred.parquet"
    td = Path(FTMIN) / f"id_bucket={b:04d}"
    if not pf.exists():
        return None
    p = pd.read_parquet(pf, columns=["ID", "FECHA", "TD_predicted"])
    tf = glob.glob(str(td / "*.parquet"))
    if not tf:
        return None
    t = pd.concat([pd.read_parquet(x, columns=["ID", "FECHA", "TMIN"]) for x in tf],
                  ignore_index=True)
    m = p.merge(t, on=["ID", "FECHA"], how="inner").dropna(subset=["TMIN"])
    if not len(m):
        return None
    v = m["TD_predicted"].to_numpy(); tm = m["TMIN"].to_numpy()
    warm = v > WARM
    out = {"n": len(m), "n_warm": int(warm.sum())}
    for k in KS:
        over = v > tm + k
        out[f"n_{k}"] = int(over.sum())
        out[f"shift_{k}"] = float((v[over] - (tm[over] + k)).sum())
        out[f"warm_fixed_{k}"] = int((warm & (v > tm + k)).sum())
    return out


def main():
    nums = sorted(int(Path(x).name.split("=")[1]) for x in glob.glob(f"{PRED}/id_bucket=*"))
    tot = Counter()
    with ProcessPoolExecutor(max_workers=14) as ex:
        for r in ex.map(one, nums, chunksize=16):
            if r:
                for k, v in r.items():
                    tot[k] += v
    n, nw = tot["n"], tot["n_warm"]
    print(f"values compared: {n:,}   values >35 C: {nw:,} ({100*nw/n:.4f}%)\n")
    print("  bound          values altered        mean shift over    share of >35 C")
    print("  Td <= Tmin+k     count      %          ALL values (C)    values removed")
    for k in KS:
        c = tot[f"n_{k}"]; s = tot[f"shift_{k}"]; w = tot[f"warm_fixed_{k}"]
        print(f"  k = {k:<3d}      {c:>12,}  {100*c/n:6.3f}%      {s/n:8.4f}"
              f"          {100*w/max(nw,1):6.2f}%")
    print("\nFor reference, capping at Td <= Tmin (k = 0) alters 79.6% of values")
    print("by a mean of 2.38 C, which is a distortion rather than a correction.")


if __name__ == "__main__":
    main()
