"""Score corrected FAO-56 baselines on the identical withheld sample.

The manuscript scores T_d = T_min in its uncorrected form. Established practice applies
an offset in arid and semi-arid regions (Allen's -2 C; see also Kimball 1997, Eccel 2012).
This evaluates the corrected variants on exactly the same observations as the main
validation, so the comparison is like for like.

Thornthwaite moisture classes: A perhumid, B humid, C subhumid, D semi-arid, E arid.
The offset is applied to classes D and E.
"""
import numpy as np
import pandas as pd

import os

RES = os.environ.get("RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")
# Scored on the leak-free backtest (selection restricted to training years), which is the
# run the manuscript reports. Override with BACKTEST_ROOT to score a different run.
ROOT = os.environ.get("BACKTEST_ROOT", f"{RES}/tuning/backtest_clean")
PRED = f"{ROOT}/ll4/predictions.parquet"

lab = (pd.read_parquet(f"{RES}/tuning/manifest.parquet")[["zone_id", "zone_label"]]
       .drop_duplicates().set_index("zone_id")["zone_label"])
moist = lab.str.strip().str[0]                      # first Thornthwaite letter
arid_zones = set(lab.index[moist.isin(["D", "E"])])
print(f"arid/semi-arid zones (classes D,E): {sorted(arid_zones)}")

df = pd.read_parquet(PRED, columns=["zone_id", "TD_obs", "pred_tuned", "pred_clim",
                                    "Tmin_hold", "pred_tmin"])
print(f"observations: {len(df):,}")

obs = df["TD_obs"].to_numpy(dtype=np.float64)
tmin = df["Tmin_hold"].to_numpy(dtype=np.float64)
is_arid = df["zone_id"].isin(arid_zones).to_numpy()

def score(pred, name):
    e = pred - obs
    ok = np.isfinite(e)
    e = e[ok]
    rmse = float(np.sqrt((e ** 2).mean())); mae = float(np.abs(e).mean()); bias = float(e.mean())
    print(f"  {name:<44} RMSE {rmse:6.3f}   MAE {mae:6.3f}   bias {bias:+7.3f}   n {ok.sum():,}")
    return rmse

print("\n=== baselines on the four-year withheld block ===")
score(df["pred_clim"].to_numpy(dtype=np.float64), "climatology")
score(df["pred_tuned"].to_numpy(dtype=np.float64), "selected model")
r_unc = score(tmin, "FAO-56 uncorrected (Td = Tmin)")
r_glob = score(tmin - 2.0, "FAO-56 with -2 C everywhere")
r_reg = score(np.where(is_arid, tmin - 2.0, tmin), "FAO-56 with -2 C in arid/semi-arid only")

# best single global offset, for reference
offs = np.arange(-4, 4.01, 0.25)
rm = [float(np.sqrt((((tmin + o) - obs) ** 2).mean())) for o in offs]
best = offs[int(np.argmin(rm))]
print(f"\n  best single global offset: {best:+.2f} C  ->  RMSE {min(rm):.3f}")

print("\n=== effect of the offset within each moisture class ===")
print("  class  n_obs        RMSE(Tmin)  RMSE(Tmin-2)  better")
for c in ["A", "B", "C", "D", "E"]:
    zs = set(lab.index[moist == c])
    m = df["zone_id"].isin(zs).to_numpy()
    if m.sum() == 0:
        continue
    a = float(np.sqrt(((tmin[m] - obs[m]) ** 2).mean()))
    b = float(np.sqrt(((tmin[m] - 2.0 - obs[m]) ** 2).mean()))
    print(f"    {c}   {m.sum():>10,}   {a:9.3f}   {b:10.3f}   {'Tmin-2' if b < a else 'Tmin'}")

print(f"\nSummary: regional correction changes FAO-56 RMSE from {r_unc:.3f} to {r_reg:.3f} C;")
print(f"         global correction gives {r_glob:.3f} C.")
