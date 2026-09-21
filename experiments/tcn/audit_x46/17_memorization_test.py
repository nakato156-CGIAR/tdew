"""Prueba directa de la hipotesis de memorizacion: una tabla de consulta
aprendida es fragil ante perturbaciones minusculas de la clave; una relacion
dinamica aprendida es suave. Se anade ruido gaussiano de amplitud creciente
a la ventana y se mide el RMSE en train y en validation, por sitio."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SITES, load_model, predict_norm, metrics, td_anom_stats, DYNAMIC_COLS, sample_windows

mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
model = load_model("last.pt")
rng = np.random.default_rng(31415)
S = {sp: sample_windows(sp, n_buckets=2, cells_per_site_per_bucket=6, seed=777, verbose=False)
     for sp in ["train", "validation"]}
for sp in S: S[sp]["site"] = S[sp]["site"].astype(str)

rows = []
for sp, s in S.items():
    obs = s["label"] * std + mean + s["td_clim"]
    for sigma in [0.0, 0.005, 0.02, 0.05, 0.1, 0.3]:
        dyn = s["dynamic"].copy()
        if sigma > 0:
            dyn[:, :, :3] += rng.normal(0, sigma, dyn[:, :, :3].shape).astype(np.float32)
        pn = predict_norm(model, s, dynamic=dyn)
        pers = dyn[:, -1, TD_IDX]
        r = {"split": sp, "sigma_ruido": sigma}
        for site in SITES:
            m = s["site"] == site
            r[f"mod_{site[:4]}"] = metrics(pn[m]*std+mean+s["td_clim"][m], obs[m])["rmse"]
            r[f"per_{site[:4]}"] = metrics(pers[m]*std+mean+s["td_clim"][m], obs[m])["rmse"]
        rows.append(r)
d = pd.DataFrame(rows)
pd.set_option("display.width", 240, "display.max_columns", 30, "display.float_format", lambda v: f"{v:.4f}")
print("RMSE (degC). mod_* = modelo, per_* = persistencia con la MISMA ventana ruidosa\n")
print(d.to_string(index=False))
d.to_csv(Path(__file__).resolve().parent / "out" / "memorization.csv", index=False)
