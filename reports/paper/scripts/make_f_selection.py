"""Figure: model-selection summary, built from the CURRENT manifest.

Panels: (a) selected day-of-year half-window h; (b) h as a function of zone and day of
year; (c) predictor retention; (d) leave-one-year-out skill gain over the fixed
five-predictor configuration.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap

RES = "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
m = pd.read_parquet(f"{RES}/tuning/manifest.parquet")
HS = [7, 11, 15, 21, 31, 45]

fig = plt.figure(figsize=(13.5, 8.4))
gs = fig.add_gridspec(2, 2, hspace=0.36, wspace=0.26)

# (a) distribution of selected h
ax = fig.add_subplot(gs[0, 0])
cnt = [int((m.h == h).sum()) for h in HS]
pct = [100 * c / len(m) for c in cnt]
ax.bar([str(h) for h in HS], pct, color="#4c72b0")
for i, (c, p) in enumerate(zip(cnt, pct)):
    ax.text(i, p + 0.6, f"{p:.1f}%", ha="center", fontsize=9)
ax.set_xlabel("selected half-window $h$ (days)"); ax.set_ylabel("% of zone-days")
ax.set_title("(a) Selected day-of-year half-window"); ax.grid(alpha=0.3, axis="y")
ax.set_ylim(0, max(pct) * 1.18)

# (b) h by zone x doy
ax = fig.add_subplot(gs[0, 1])
piv = m.pivot_table(index="zone_id", columns="doy", values="h", aggfunc="first")
cmap = ListedColormap(plt.cm.viridis(np.linspace(0, 1, len(HS))))
norm = BoundaryNorm([0] + [ (HS[i]+HS[i+1])/2 for i in range(len(HS)-1) ] + [60], cmap.N)
im = ax.pcolormesh(piv.columns.values, piv.index.values, piv.values, cmap=cmap, norm=norm)
ax.set_xlabel("day of year"); ax.set_ylabel("climate zone")
ax.set_title("(b) Selected $h$ by zone and day of year")
cb = fig.colorbar(im, ax=ax, ticks=HS, pad=0.02); cb.set_label("$h$ (days)", fontsize=9)

# (c) predictor retention
ax = fig.add_subplot(gs[1, 0])
feats = {}
for fl in m.feature_list:
    for f in str(fl).split(","):
        feats[f] = feats.get(f, 0) + 1
order = ["const", "TMIN_anom", "TMIN_anom_lag1", "TMIN_anom_lag2", "TMIN_anom_lag7",
         "TMIN_anom_lag30", "TD_anom_lag1", "TD_anom_lag2", "TD_anom_lag3",
         "TD_anom_lag7", "TD_anom_lag30"]
order = [f for f in order if f in feats]
vals = [100 * feats[f] / len(m) for f in order]
lbl = [f.replace("_anom", "").replace("TMIN", "Tmin").replace("TD", "Td").replace("_lag", " lag ")
       for f in order]
ax.barh(lbl[::-1], vals[::-1], color="#55a868")
ax.set_xlabel("% of zone-days retaining the predictor"); ax.set_xlim(0, 104)
ax.set_title("(c) Predictor retention"); ax.grid(alpha=0.3, axis="x")

# (d) skill gain over the fixed five-predictor configuration
ax = fig.add_subplot(gs[1, 1])
up = (m.skill - m.skill_baseline)
ax.hist(up, bins=60, color="#c44e52")
ax.axvline(0, color="k", lw=1)
ax.set_xlabel("LOYOCV skill gain over fixed five-predictor model")
ax.set_ylabel("zone-days")
ax.set_title("(d) Skill gain from selection")
ax.grid(alpha=0.3, axis="y")
ax.text(0.97, 0.95, f"mean {up.mean():+.4f}\nmedian {up.median():+.4f}\n"
        f"$\\leq$0 for {100*(up<=0).mean():.1f}%",
        transform=ax.transAxes, ha="right", va="top", fontsize=9,
        bbox=dict(boxstyle="round", fc="white", alpha=0.85))

out = f"{OUT}/F0_model_selection.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("wrote", out)
print(f"recipes={len(m)}  zones={m.zone_id.nunique()}  h=45 share={100*(m.h==45).mean():.1f}%")
