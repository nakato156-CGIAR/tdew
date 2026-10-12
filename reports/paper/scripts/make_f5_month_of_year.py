"""F5: warm-tail exceedances by month of year, from warm_tail_diagnostics.py output.

Requires warm_tail_monthly.json (written by warm_tail_diagnostics.py). Cheap - no data scan.
"""
import json, collections, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SRC = sys.argv[1] if len(sys.argv) > 1 else ".asta/theories/warm_tail_monthly.json"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
d = json.load(open(SRC))
years = [2017, 2018, 2019, 2020]
rate = {}
for y in years:
    for m in range(1, 13):
        k = f"{y}{m:02d}"
        n, g = d["ym_n"].get(k, 0), d["ym_gt35"].get(k, 0)
        rate[(y, m)] = 100 * g / n if n else 0.0
mn, mg = collections.Counter(), collections.Counter()
for k, v in d["ym_n"].items():
    mn[int(k) % 100] += v
for k, v in d["ym_gt35"].items():
    mg[int(k) % 100] += v
pooled = [100 * mg[m] / mn[m] if mn[m] else 0 for m in range(1, 13)]

ML = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
fig, axs = plt.subplots(1, 2, figsize=(13, 4.6))
ax = axs[0]
ax.bar(ML, pooled, color=["#c44e52" if m == 11 else "#9fb8d4" for m in range(1, 13)])
ax.set_ylabel("% of values > 35 °C"); ax.grid(alpha=0.3, axis="y")
ax.set_title("Pooled 2017–2020: exceedances by month of year")
for i, v in enumerate(pooled):
    if v > 0.001:
        ax.text(i, v + 0.03, f"{v:.3f}", ha="center", fontsize=8)
ax.annotate(f"Nov = {pooled[10]:.3f}%\n({pooled[10]/pooled[9]:.0f}× October;\nzero Jan–Jul)",
            xy=(10, pooled[10]), xytext=(5.2, 1.05), fontsize=9,
            arrowprops=dict(arrowstyle="->", lw=1))
ax = axs[1]
w = 0.2
for i, y in enumerate(years):
    ax.bar(np.arange(12) + (i - 1.5) * w, [rate[(y, m)] for m in range(1, 13)],
           width=w, label=str(y))
ax.set_xticks(range(12)); ax.set_xticklabels(ML)
ax.set_ylabel("% of values > 35 °C"); ax.grid(alpha=0.3, axis="y")
ax.set_title("By year: the November spike recurs, magnitude varies"); ax.legend(fontsize=8)
fig.suptitle("Warm tail (>35 °C) is confined almost entirely to November", fontsize=12.5)
fig.tight_layout(rect=[0, 0, 1, 0.93])
fig.savefig(f"{OUT}/F5_warm_tail_month_of_year.png", dpi=150)
print("wrote", f"{OUT}/F5_warm_tail_month_of_year.png")
