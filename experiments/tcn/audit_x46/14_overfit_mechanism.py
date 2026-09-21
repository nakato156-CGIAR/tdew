"""Por que el modelo alcanza RMSE 0.147 degC en train para Loreto y 1.11 en
validation, mientras persistencia y climatologia solo se degradan 1.1x.

Se prueban dos mecanismos:
 (1) las covariables del dia objetivo (target_cond: LST_DAY/LST_NIGHT en t+1)
     contienen el objetivo casi exactamente en el periodo de entrenamiento;
 (2) la relacion es lineal y esta en los datos (un OLS la reproduce).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, TARGET_COND_COLS, sample_windows)

OUT = Path(__file__).resolve().parent / "out"
mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
model = load_model("last.pt")
S = {sp: sample_windows(sp, n_buckets=4, cells_per_site_per_bucket=8, seed=777, verbose=False)
     for sp in ["train", "validation"]}
for sp in S: S[sp]["site"] = S[sp]["site"].astype(str)

print("=== 1. ablacion de target_cond por sitio y split (modelo entrenado, last.pt) ===")
rows = []
for sp, s in S.items():
    base = predict_norm(model, s)
    noTC = predict_norm(model, s, target_cond=np.zeros_like(s["target_cond"]))
    tc = s["target_cond"].copy(); tc[:, 2:] = 0.0
    noLST = predict_norm(model, s, target_cond=tc)
    noDYN = predict_norm(model, s, dynamic=np.zeros_like(s["dynamic"]))
    obs = s["label"] * std + mean + s["td_clim"]
    for site in SITES:
        m = s["site"] == site
        f = lambda p: metrics(p[m] * std + mean + s["td_clim"][m], obs[m])["rmse"]
        rows.append({"split": sp, "sitio": site, "rmse_base": f(base),
                     "sin_target_cond": f(noTC), "sin_LST(t+1)": f(noLST),
                     "sin_dynamic": f(noDYN)})
d = pd.DataFrame(rows)
pd.set_option("display.width", 220, "display.float_format", lambda v: f"{v:.4f}")
print(d.to_string(index=False))

print("\n=== 2. correlacion del objetivo con cada covariable del dia t+1 ===")
rows = []
for sp, s in S.items():
    for site in SITES:
        m = s["site"] == site
        r = {"split": sp, "sitio": site}
        for j, c in enumerate(TARGET_COND_COLS):
            r[f"corr_{c}"] = float(np.corrcoef(s["label"][m], s["target_cond"][m][:, j])[0, 1])
        r["corr_TD_anom(t)"] = float(np.corrcoef(s["label"][m], s["dynamic"][m][:, -1, TD_IDX])[0, 1])
        r["std_LST_NIGHT(t+1)"] = float(s["target_cond"][m][:, 3].std())
        r["frac_LST_NIGHT==0"] = float((s["target_cond"][m][:, 3] == 0).mean())
        rows.append(r)
print(pd.DataFrame(rows).to_string(index=False))

print("\n=== 3. un OLS con las mismas entradas, ajustado SOLO con train de cada sitio ===")
def design(s, m, with_tc=True):
    n = int(m.sum()); parts = [s["dynamic"][m].reshape(n, -1), s["static"][m]]
    if with_tc: parts.append(s["target_cond"][m])
    return np.c_[np.ones(n), np.concatenate([p.astype(np.float64) for p in parts], 1)]
rows = []
for site in SITES:
    mt = S["train"]["site"] == site; mv = S["validation"]["site"] == site
    for with_tc in [True, False]:
        Xt, yt = design(S["train"], mt, with_tc), S["train"]["label"][mt].astype(np.float64)
        w = np.linalg.lstsq(Xt, yt, rcond=None)[0]
        def rm(s, m, X):
            o = s["label"][m] * std + mean + s["td_clim"][m]
            return metrics((X @ w) * std + mean + s["td_clim"][m], o)["rmse"]
        rows.append({"sitio": site, "target_cond": with_tc,
                     "rmse_train_in_sample": rm(S["train"], mt, Xt),
                     "rmse_validation": rm(S["validation"], mv, design(S["validation"], mv, with_tc))})
print(pd.DataFrame(rows).to_string(index=False))
