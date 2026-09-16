"""Warm-tail diagnostics: discriminate AR drift vs seasonal-regime mechanism,
and quantify the physical-bound violation (Td_pred vs same-day Tmin).

Single parallel pass over all 8192 buckets. Read-only.
"""
import glob, os, json
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd

RES = "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"
PRED = f"{RES}/tuning/predictions_2017_2020"
FTMIN = f"{RES}/future_tmin_by_bucket"
WARM = 35.0


def one(bnum):
    pf = Path(PRED) / f"id_bucket={bnum:04d}" / "pred.parquet"
    if not pf.exists():
        return None
    p = pd.read_parquet(pf, columns=["ID", "FECHA", "TD_predicted"])
    p["FECHA"] = pd.to_datetime(p["FECHA"])
    d = p["FECHA"]
    yr = d.dt.year.to_numpy()
    ym = (d.dt.year * 100 + d.dt.month).to_numpy()
    v = p["TD_predicted"].to_numpy()

    out = {}
    # (1) per-year totals and exceedances
    out["year_n"] = Counter(dict(pd.Series(v).groupby(yr).count()))
    out["year_gt35"] = Counter(dict(pd.Series((v > WARM).astype("int64")).groupby(yr).sum()))
    out["year_gt32"] = Counter(dict(pd.Series((v > 32).astype("int64")).groupby(yr).sum()))
    # per-month exceedance (seasonality)
    out["ym_n"] = Counter(dict(pd.Series(v).groupby(ym).count()))
    out["ym_gt35"] = Counter(dict(pd.Series((v > WARM).astype("int64")).groupby(ym).sum()))

    # (2) physical bound: compare with same-day future Tmin
    td = Path(FTMIN) / f"id_bucket={bnum:04d}"
    tf = glob.glob(str(td / "*.parquet"))
    if tf:
        t = pd.concat([pd.read_parquet(x, columns=["ID", "FECHA", "TMIN"]) for x in tf],
                      ignore_index=True)
        t["FECHA"] = pd.to_datetime(t["FECHA"])
        m = p.merge(t, on=["ID", "FECHA"], how="inner").dropna(subset=["TMIN"])
        if len(m):
            exc = (m["TD_predicted"] - m["TMIN"]).to_numpy()
            out["n_cmp"] = len(m)
            out["n_td_gt_tmin"] = int((exc > 0).sum())
            out["exc_sum"] = float(exc[exc > 0].sum())
            # excess histogram (0-15 C, 0.5 bins)
            out["exc_hist"] = np.histogram(exc, bins=np.arange(-20, 20.01, 0.5))[0]
            # among the >35C warm-tail values specifically
            w = m["TD_predicted"].to_numpy() > WARM
            out["n_warm_cmp"] = int(w.sum())
            out["n_warm_gt_tmin"] = int((exc[w] > 0).sum())
            out["warm_exc_mean"] = float(exc[w].mean()) if w.any() else float("nan")
            # effect of capping Td at Tmin
            capped = np.minimum(m["TD_predicted"].to_numpy(), m["TMIN"].to_numpy())
            out["n_changed_by_cap"] = int((capped < m["TD_predicted"].to_numpy()).sum())
            out["cap_delta_sum"] = float((m["TD_predicted"].to_numpy() - capped).sum())
            out["cap_n"] = len(m)

    # (3) clustering: longest consecutive run of >WARM days per cell
    p2 = p.sort_values(["ID", "FECHA"])
    flag = (p2["TD_predicted"].to_numpy() > WARM)
    if flag.any():
        ids = p2["ID"].to_numpy()
        # run-length encode within each ID
        brk = np.empty(len(flag), dtype=bool); brk[0] = True
        brk[1:] = (ids[1:] != ids[:-1]) | (flag[1:] != flag[:-1])
        grp = np.cumsum(brk) - 1
        lens = np.bincount(grp)
        isw = flag[brk]
        runs = lens[isw]
        out["run_hist"] = Counter(dict(zip(*np.unique(runs, return_counts=True))))
    return out


def merge_counter(a, b):
    for k, val in b.items():
        a[k] = a.get(k, 0) + val
    return a


def main():
    nums = sorted(int(Path(x).name.split("=")[1]) for x in glob.glob(f"{PRED}/id_bucket=*"))
    print(f"buckets: {len(nums)}", flush=True)
    agg = {"year_n": {}, "year_gt35": {}, "year_gt32": {}, "ym_n": {}, "ym_gt35": {}, "run_hist": {}}
    scal = {k: 0.0 for k in ["n_cmp", "n_td_gt_tmin", "exc_sum", "n_warm_cmp", "n_warm_gt_tmin",
                             "n_changed_by_cap", "cap_delta_sum", "cap_n"]}
    exc_hist = np.zeros(80, dtype=np.int64)
    warm_exc_w, warm_exc_s = 0, 0.0
    with ProcessPoolExecutor(max_workers=14) as ex:
        for r in ex.map(one, nums, chunksize=16):
            if r is None:
                continue
            for k in agg:
                if k in r:
                    merge_counter(agg[k], r[k])
            for k in scal:
                if k in r:
                    scal[k] += r[k]
            if "exc_hist" in r:
                exc_hist += r["exc_hist"]
            if r.get("n_warm_cmp", 0) and not np.isnan(r.get("warm_exc_mean", np.nan)):
                warm_exc_w += r["n_warm_cmp"]; warm_exc_s += r["warm_exc_mean"] * r["n_warm_cmp"]

    print("\n=== (1) AR DRIFT TEST: >35C incidence by year ===")
    print("  year      n_values      n>35C     pct>35C     pct>32C")
    for y in sorted(agg["year_n"]):
        n = agg["year_n"][y]; g35 = agg["year_gt35"].get(y, 0); g32 = agg["year_gt32"].get(y, 0)
        print(f"  {y}   {n:>12,}  {g35:>10,}   {100*g35/n:>8.4f}%   {100*g32/n:>8.4f}%")
    print("  -> monotonic growth would support AR error accumulation;")
    print("     flat/non-monotonic supports the seasonal-regime mechanism.")

    print("\n=== (1b) seasonality: months with highest >35C rate ===")
    rates = {k: 100*agg["ym_gt35"].get(k, 0)/v for k, v in agg["ym_n"].items() if v}
    for k in sorted(rates, key=lambda z: -rates[z])[:12]:
        print(f"  {k}: {rates[k]:.3f}%   (n>35C={agg['ym_gt35'].get(k,0):,})")

    print("\n=== (2) PHYSICAL BOUND: predicted Td vs same-day Tmin ===")
    if scal["n_cmp"]:
        print(f"  compared values           : {int(scal['n_cmp']):,}")
        print(f"  Td_pred > Tmin            : {int(scal['n_td_gt_tmin']):,} "
              f"({100*scal['n_td_gt_tmin']/scal['n_cmp']:.3f}%)")
        print(f"  mean excess when exceeding: {scal['exc_sum']/max(scal['n_td_gt_tmin'],1):.3f} C")
        if scal["n_warm_cmp"]:
            print(f"  of the >35C values ({int(scal['n_warm_cmp']):,}): "
                  f"{int(scal['n_warm_gt_tmin']):,} exceed same-day Tmin "
                  f"({100*scal['n_warm_gt_tmin']/scal['n_warm_cmp']:.2f}%)")
            print(f"  mean (Td_pred - Tmin) for >35C values: {warm_exc_s/max(warm_exc_w,1):.3f} C")
        print(f"\n  --- effect of capping Td at Tmin ---")
        print(f"  values changed : {int(scal['n_changed_by_cap']):,} "
              f"({100*scal['n_changed_by_cap']/scal['cap_n']:.3f}%)")
        print(f"  mean shift over ALL values: {scal['cap_delta_sum']/scal['cap_n']:.4f} C")

    print("\n=== (3) CLUSTERING: run lengths of consecutive >35C days per cell ===")
    rh = agg["run_hist"]
    tot = sum(rh.values())
    print(f"  total runs: {tot:,}")
    for L in sorted(rh)[:10]:
        print(f"    {L:>3d}-day runs: {rh[L]:>9,}  ({100*rh[L]/tot:5.2f}%)")
    if rh:
        mx = max(rh); print(f"  longest run: {mx} days")
        w = sum(L*c for L, c in rh.items()); print(f"  mean run length: {w/tot:.2f} days")
    with open(".asta/theories/warm_tail_monthly.json","w") as fh:
        json.dump({"ym_n":{str(k):int(v) for k,v in agg["ym_n"].items()},
                   "ym_gt35":{str(k):int(v) for k,v in agg["ym_gt35"].items()},
                   "year_n":{str(k):int(v) for k,v in agg["year_n"].items()},
                   "year_gt35":{str(k):int(v) for k,v in agg["year_gt35"].items()},
                   "run_hist":{str(k):int(v) for k,v in agg["run_hist"].items()}}, fh)
    print("wrote .asta/theories/warm_tail_monthly.json")
    print("\nDIAGNOSTICS DONE")


if __name__ == "__main__":
    main()
