"""Diagnose the November warm-tail concentration.

Three tests, all internal to our own model and product:

  T1  WHICH ZONES/DOYS. Locate exceedances (>35 C) in (zone, year, day-of-year) space.
  T2  DOES THE PEAK DAY MOVE BETWEEN YEARS? Onset misalignment implies the exceedance peak
      shifts year to year (onset date is interannually variable); a structural defect in
      particular day-of-year recipes implies it fires on the SAME doys every year.
  T3  IS NOVEMBER ALREADY POORLY FIT IN-SAMPLE? Compare LOYOCV skill (manifest) and
      r_squared_anom (coeffs) for November doys against adjacent bands, in the affected zones.
      The regime/onset mechanism predicts degraded in-sample fit there; a purely structural
      recipe defect need not.
"""
import glob, os
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
import pandas as pd

RES = "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"
PRED = f"{RES}/tuning/predictions_2017_2020"
COEF = f"{RES}/tuning/zoned_coeffs"
WARM = 35.0


def scan(bnum):
    pf = Path(PRED) / f"id_bucket={bnum:04d}" / "pred.parquet"
    if not pf.exists():
        return None
    p = pd.read_parquet(pf, columns=["ID", "FECHA", "TD_predicted"])
    m = p["TD_predicted"].to_numpy() > WARM
    if not m.any():
        return {"ydoy": Counter(), "ids": np.array([], dtype=np.int64)}
    d = pd.to_datetime(p["FECHA"][m])
    return {"ydoy": Counter(zip(d.dt.year.to_numpy(), d.dt.dayofyear.to_numpy())),
            "ids": p["ID"].to_numpy()[m]}


def main():
    nums = sorted(int(Path(x).name.split("=")[1]) for x in glob.glob(f"{PRED}/id_bucket=*"))
    ydoy = Counter(); ids = []
    with ProcessPoolExecutor(max_workers=14) as ex:
        for r in ex.map(scan, nums, chunksize=16):
            if r:
                ydoy.update(r["ydoy"])
                if len(r["ids"]):
                    ids.append(r["ids"])
    ids = np.unique(np.concatenate(ids)) if ids else np.array([], dtype=np.int64)
    print(f"exceedances: {sum(ydoy.values()):,}   affected cells: {len(ids):,}", flush=True)

    # ---- T1: zones ----
    zt = pd.read_parquet(f"{RES}/zone_table.parquet")
    zcol = "zone_id" if "zone_id" in zt.columns else zt.columns[1]
    aff = zt[zt["ID"].isin(ids)]
    zc = aff[zcol].value_counts()
    print("\n=== T1  affected cells by zone (top 8) ===")
    tot_by_zone = zt[zcol].value_counts()
    for z, c in zc.head(8).items():
        print(f"  zone {z}: {c:,} affected of {tot_by_zone.get(z,0):,} cells "
              f"({100*c/max(tot_by_zone.get(z,1),1):.1f}% of zone)")
    top_zones = list(zc.head(3).index)

    # ---- T2: does the peak day move between years? ----
    print("\n=== T2  day-of-year distribution of exceedances, by year ===")
    print("  year   n_exceed   peak_doy  peak_date   mean_doy   p10-p90 doy")
    for y in [2017, 2018, 2019, 2020]:
        sub = {k[1]: v for k, v in ydoy.items() if k[0] == y}
        if not sub:
            print(f"  {y}   (none)"); continue
        doys = np.array(sorted(sub)); cnts = np.array([sub[d] for d in doys])
        pk = int(doys[np.argmax(cnts)])
        mean_doy = float((doys * cnts).sum() / cnts.sum())
        cum = np.cumsum(cnts) / cnts.sum()
        p10 = int(doys[np.searchsorted(cum, .10)]); p90 = int(doys[np.searchsorted(cum, .90)])
        date = (pd.Timestamp(f"{y}-01-01") + pd.Timedelta(days=pk - 1)).strftime("%d %b")
        print(f"  {y}   {cnts.sum():>9,}   {pk:>7d}  {date:>9}   {mean_doy:8.1f}   {p10:>3d}-{p90:<3d}")
    print("  -> a peak that MOVES between years supports onset misalignment;")
    print("     a peak fixed on the same doys supports a structural recipe defect.")

    # ---- T3: in-sample fit by doy in the affected zones ----
    man = pd.read_parquet(f"{RES}/tuning/manifest.parquet")
    mz = man[man["zone_id"].isin(top_zones)]
    def band(lo, hi):
        b = mz[(mz["doy"] >= lo) & (mz["doy"] <= hi)]
        return (b["skill"].mean(), (b["skill"] - b["skill_baseline"]).mean(),
                b["h"].median(), b["n_features"].mean(), len(b))
    print("\n=== T3a  LOYOCV skill by day-of-year band (affected zones, manifest) ===")
    print("  band            doy        skill   uplift   med_h  n_feat   n")
    for lab, lo, hi in [("Aug-Sep", 213, 273), ("Oct", 274, 304), ("NOVEMBER", 305, 334),
                        ("Dec", 335, 365), ("Jan-Jul", 1, 212)]:
        sk, up, hh, nf, n = band(lo, hi)
        print(f"  {lab:<12} {lo:>3d}-{hi:<3d}   {sk:8.4f} {up:+8.4f}  {hh:5.0f}  {nf:5.2f}  {n:>4d}")

    # ---- T3b: r_squared_anom by doy from a sample of coeff buckets ----
    print("\n=== T3b  in-sample R^2 by doy band (affected zones, 24 coeff buckets) ===")
    zmap = zt.set_index("ID")[zcol]
    rows = []
    for b in nums[::341][:24]:
        f = Path(COEF) / f"id_bucket={b:04d}" / "coeffs.parquet"
        if not f.exists():
            continue
        c = pd.read_parquet(f, columns=["ID", "zone_id", "doy", "r_squared_anom"])
        c = c[c["zone_id"].isin(top_zones)].drop_duplicates(["ID", "doy"])
        if len(c):
            rows.append(c)
    if rows:
        c = pd.concat(rows, ignore_index=True)
        print("  band            doy        mean_R2   median_R2      n")
        for lab, lo, hi in [("Aug-Sep", 213, 273), ("Oct", 274, 304), ("NOVEMBER", 305, 334),
                            ("Dec", 335, 365), ("Jan-Jul", 1, 212)]:
            sub = c[(c["doy"] >= lo) & (c["doy"] <= hi)]["r_squared_anom"]
            if len(sub):
                print(f"  {lab:<12} {lo:>3d}-{hi:<3d}   {sub.mean():9.4f}   {sub.median():9.4f}  {len(sub):>7,}")
    else:
        print("  (no coeff rows for the affected zones in the sampled buckets)")
    print("\nNOVEMBER DIAGNOSTICS DONE")


if __name__ == "__main__":
    main()
