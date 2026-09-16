"""Test the training period for non-stationarity in the Tmin-to-Td relationship.

The reconstruction extrapolates four years forward on coefficients fitted to 1981-2016,
which assumes the relationship is stable. Two things could drift and they have different
consequences, so both are tested separately:

  (a) the level of each field, which a trend in the fitted climatology would absorb only
      partly, since the climatology is a fixed day-of-year mean;
  (b) the regression slope of the dew-point anomaly on the minimum-temperature anomaly,
      which is the quantity the model actually carries forward.

Anomalies for (b) are taken against each half's own day-of-year climatology, so a shift in
level cannot masquerade as a shift in slope.

Results are stratified by support tier, because the source product is weakly constrained
far from the station network and drift there need not mean drift where the product is used.

Prints a table per tier; writes nothing.
"""
import glob
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

RES = os.environ.get("RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")
PREPARED = f"{RES}/bucketed_training_data"
SPLIT_YEAR = 1998          # 1981-1998 vs 1999-2016, equal halves of the 36-year record
BUCKET_STRIDE = int(os.environ.get("BUCKET_STRIDE", "128"))
TIERS = ["within", "near", "marginal", "extrapolated", "unsupported"]


def _one_bucket(b: int):
    """Per-cell statistics for one bucket: level trends and per-half regression slopes."""
    fs = glob.glob(f"{PREPARED}/id_bucket={b:04d}/*.parquet")
    if not fs:
        return None
    d = pd.concat([pd.read_parquet(f, columns=["ID", "FECHA", "TD", "TMIN"]) for f in fs],
                  ignore_index=True)
    d = d.dropna(subset=["TD", "TMIN"])
    if d.empty:
        return None
    t = pd.to_datetime(d["FECHA"])
    d["year"] = t.dt.year.to_numpy()
    d["doy"] = t.dt.dayofyear.to_numpy()
    d["half"] = (d["year"] > SPLIT_YEAR).astype(np.int8)

    # (a) level: per-cell linear trend of the annual mean, in C per decade
    ann = d.groupby(["ID", "year"])[["TD", "TMIN"]].mean().reset_index()
    out = []
    for col in ("TD", "TMIN"):
        # OLS slope of the annual mean against year
        x = ann["year"].to_numpy(dtype=float)
        y = ann[col].to_numpy(dtype=float)
        ids = ann["ID"].to_numpy()
        df = pd.DataFrame({"ID": ids, "x": x, "y": y})
        s = df.groupby("ID").apply(
            lambda t: np.polyfit(t.x, t.y, 1)[0] * 10.0, include_groups=False)
        out.append(s.rename(f"trend_{col}"))
    trends = pd.concat(out, axis=1)

    # (b) slope: anomalies against each half's own day-of-year climatology
    clim = d.groupby(["ID", "half", "doy"])[["TD", "TMIN"]].transform("mean")
    d["tda"] = d["TD"] - clim["TD"]
    d["tma"] = d["TMIN"] - clim["TMIN"]
    d["xy"] = d["tma"] * d["tda"]
    d["xx"] = d["tma"] * d["tma"]
    acc = d.groupby(["ID", "half"])[["xy", "xx"]].sum()
    acc["slope"] = acc["xy"] / acc["xx"].where(acc["xx"] > 0)
    sl = acc["slope"].unstack("half")
    sl.columns = ["slope_early", "slope_late"]
    return trends.join(sl, how="inner")


def main() -> int:
    buckets = sorted(range(0, 8192, BUCKET_STRIDE))
    print(f"sampling {len(buckets)} buckets (stride {BUCKET_STRIDE}), "
          f"halves 1981-{SPLIT_YEAR} vs {SPLIT_YEAR + 1}-2016")
    with ProcessPoolExecutor(12) as ex:
        parts = [p for p in ex.map(_one_bucket, buckets, chunksize=2) if p is not None]
    cells = pd.concat(parts)
    sd = pd.read_parquet(f"{RES}/tuning/support_distance.parquet", columns=["ID", "tier"])
    j = cells.join(sd.set_index("ID"), how="inner").dropna(
        subset=["slope_early", "slope_late"])
    j["d_slope"] = j["slope_late"] - j["slope_early"]
    print(f"cells with both halves: {len(j):,}\n")

    print("=== (a) level trend, C per decade, and (b) change in Tmin-to-Td slope ===")
    print(f"{'tier':>14} {'cells':>8} {'trend Td':>10} {'trend Tmin':>11} "
          f"{'slope early':>12} {'slope late':>11} {'change':>8} {'% cells up':>11}")
    for t in TIERS + ["ALL"]:
        s = j if t == "ALL" else j[j.tier == t]
        if not len(s):
            continue
        print(f"{t:>14} {len(s):>8,} {s.trend_TD.mean():>10.4f} {s.trend_TMIN.mean():>11.4f} "
              f"{s.slope_early.mean():>12.4f} {s.slope_late.mean():>11.4f} "
              f"{s.d_slope.mean():>8.4f} {100 * (s.d_slope > 0).mean():>10.1f}%")

    # Is the slope change large relative to its spread across cells?
    a = j[j.tier == "within"]
    print(f"\nwithin the classified domain: slope change mean {a.d_slope.mean():+.4f}, "
          f"sd {a.d_slope.std():.4f}, median {a.d_slope.median():+.4f}")
    print(f"  cells whose slope changed by more than 0.1: "
          f"{100 * (a.d_slope.abs() > 0.1).mean():.1f}%")
    print(f"  Cohen's d of the change: {a.d_slope.mean() / a.d_slope.std():.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
