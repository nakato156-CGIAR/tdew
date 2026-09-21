"""Compara, sobre EXACTAMENTE las mismas ventanas de validation, el modelo
profundo entrenado contra predictores triviales y contra un ajuste lineal
por minimos cuadrados sobre las mismas entradas que recibe el TCN.

Las metricas por sitio se agregan a un 'ALL' reponderado con el numero real
de celdas por sitio (leido de Data/silver/department_grid_ids/*.csv), para
que sea comparable con las filas site=ALL del leaderboard, que estan
dominadas por Loreto.
"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd, torch
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, STATIC_COLS, TARGET_COND_COLS, DEFAULT_SILVER_DIR, CKDIR)

OUT = Path(__file__).resolve().parent / "out"
val = dict(np.load(OUT / "sample_validation.npz", allow_pickle=False))
tr = dict(np.load(OUT / "sample_train.npz", allow_pickle=False))
val["site"] = val["site"].astype(str); tr["site"] = tr["site"].astype(str)
mean, std = td_anom_stats()
print(f"TD_anom mean={mean:.4g} std={std:.6f}  (Data/gold/normalization_stats.json)")
print("DYNAMIC_COLS =", DYNAMIC_COLS)
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")

# n real de celdas por sitio, leido de los CSV de grid ids
ncells = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / "department_grid_ids" / f"{s}.csv")) for s in SITES}
print("celdas por sitio (Data/silver/department_grid_ids):", ncells)

obs = val["label"] * std + mean + val["td_clim"]

preds = {}
preds["climatology"] = np.zeros_like(val["label"])
preds["persistence(TD_anom t)"] = val["dynamic"][:, -1, TD_IDX].copy()
preds["media_ultimos_3d"] = val["dynamic"][:, -3:, TD_IDX].mean(1)
preds["media_ventana_31d"] = val["dynamic"][:, :, TD_IDX].mean(1)

for ck in ["best.pt", "epoch_0000.pt", "epoch_0001.pt", "epoch_0002.pt", "epoch_0003.pt", "epoch_0004.pt"]:
    if (CKDIR / ck).exists():
        preds[f"TCN {ck}"] = predict_norm(load_model(ck), val)

# --- lineal por minimos cuadrados sobre las MISMAS entradas del TCN ---
def design(s):
    n = len(s["label"])
    reg = np.zeros((n, 3), dtype=np.float64); reg[np.arange(n), s["region"]] = 1.0
    return np.concatenate([np.ones((n, 1)), s["dynamic"].reshape(n, -1).astype(np.float64),
                           s["static"].astype(np.float64), reg[:, 1:], s["target_cond"].astype(np.float64)], axis=1)

Xtr, ytr = design(tr), tr["label"].astype(np.float64)
coef = np.linalg.lstsq(Xtr, ytr, rcond=None)[0]
preds["OLS mismas entradas (fit en train)"] = design(val) @ coef
print(f"OLS: {Xtr.shape[1]} regresores, ajustado sobre {len(ytr)} ventanas de train")

# --- lineal solo con los rezagos de TD (analogo al pool de los baselines) ---
def design_lag(s):
    n = len(s["label"])
    td = s["dynamic"][:, :, TD_IDX].astype(np.float64)
    lags = np.stack([td[:, -1], td[:, -2], td[:, -3], td[:, -7], td[:, -30]], 1)
    return np.concatenate([np.ones((n, 1)), lags], 1)
coef2 = np.linalg.lstsq(design_lag(tr), ytr, rcond=None)[0]
preds["OLS solo rezagos TD"] = design_lag(val) @ coef2

rows = []
for name, pn in preds.items():
    phys = pn * std + mean + val["td_clim"]
    per_site = {}
    for s in SITES:
        m = val["site"] == s
        per_site[s] = metrics(phys[m], obs[m])
    # ALL sin reponderar (submuestra balanceada) y reponderado por celdas reales
    mse_bal = np.mean([per_site[s]["rmse"] ** 2 for s in SITES])
    tot = sum(ncells.values())
    mse_w = sum(ncells[s] / tot * per_site[s]["rmse"] ** 2 for s in SITES)
    rows.append({"predictor": name,
                 **{f"rmse_{s}": per_site[s]["rmse"] for s in SITES},
                 "rmse_ALL_submuestra_balanceada": np.sqrt(mse_bal),
                 "rmse_ALL_reponderado_por_celdas": np.sqrt(mse_w),
                 "mae_ALL_repond": sum(ncells[s]/tot * per_site[s]["mae"] for s in SITES),
                 "bias_ALL_repond": sum(ncells[s]/tot * per_site[s]["bias"] for s in SITES)})

df = pd.DataFrame(rows)
pd.set_option("display.width", 250, "display.max_columns", 50, "display.float_format", lambda v: f"{v:.4f}")
print("\n=== RMSE (degC) sobre las MISMAS 559.200 ventanas de validation ===")
print(df.to_string(index=False))
df.to_csv(OUT / "compare_predictors.csv", index=False)

clim_w = df.loc[df.predictor == "climatology", "rmse_ALL_reponderado_por_celdas"].iloc[0]
print(f"\nskill_vs_clim (ALL reponderado), clim_rmse={clim_w:.6f}:")
for _, r in df.iterrows():
    print(f"   {r.predictor:38s} {1 - r['rmse_ALL_reponderado_por_celdas']/clim_w:+.4f}")
