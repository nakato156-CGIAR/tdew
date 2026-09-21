"""El modelo alcanza RMSE 0.147 degC en train para Loreto y 1.08 degC en
validation. Se distingue si eso es memorizacion del modelo o una propiedad
de los datos, comparando predictores SIN parametros (climatologia,
persistencia) en los dos splits sobre las mismas celdas.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, sample_windows)

OUT = Path(__file__).resolve().parent / "out"
mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
model = load_model("last.pt")

# mismas celdas en los tres splits: se reusa la misma semilla de bucket/celda
res = []
for split in ["train", "validation", "test"]:
    s = sample_windows(split, n_buckets=4, cells_per_site_per_bucket=8, seed=777, verbose=False)
    s["site"] = s["site"].astype(str)
    pn = predict_norm(model, s)
    obs = s["label"] * std + mean + s["td_clim"]
    for site in SITES:
        m = s["site"] == site
        row = {"split": split, "sitio": site, "n": int(m.sum()),
               "celdas": int(len(np.unique(s["id"][m]))),
               "std_TD_anom_norm": float(s["label"][m].std()),
               "std_TD_clim": float(s["td_clim"][m].std()),
               "rmse_clim": metrics((0*pn[m])*std+mean+s["td_clim"][m], obs[m])["rmse"],
               "rmse_persistencia": metrics(s["dynamic"][m][:, -1, TD_IDX]*std+mean+s["td_clim"][m], obs[m])["rmse"],
               "rmse_modelo": metrics(pn[m]*std+mean+s["td_clim"][m], obs[m])["rmse"],
               "autocorr_lag1": float(np.corrcoef(s["label"][m], s["dynamic"][m][:, -1, TD_IDX])[0, 1])}
        res.append(row)
df = pd.DataFrame(res)
pd.set_option("display.width", 220, "display.float_format", lambda v: f"{v:.4f}")
print("mismas celdas (seed=777, 4 buckets x 8 celdas/sitio) en los tres splits\n")
print(df.to_string(index=False))
df.to_csv(OUT / "train_val_gap.csv", index=False)

print("\n=== razon modelo validation / modelo train, y lo mismo para persistencia ===")
p = df.pivot(index="sitio", columns="split")
for site in SITES:
    r = df[df.sitio == site].set_index("split")
    print(f"   {site:22s} modelo v/t={r.loc['validation','rmse_modelo']/r.loc['train','rmse_modelo']:6.2f}  "
          f"persistencia v/t={r.loc['validation','rmse_persistencia']/r.loc['train','rmse_persistencia']:6.2f}  "
          f"clim v/t={r.loc['validation','rmse_clim']/r.loc['train','rmse_clim']:6.2f}  "
          f"std_anom v/t={r.loc['validation','std_TD_anom_norm']/r.loc['train','std_TD_anom_norm']:6.2f}")
