"""Sondas lineales sobre las representaciones internas del modelo ENTRENADO.

Localizan en que punto del grafo se pierde la informacion: si una regresion
lineal sobre la salida del TCN ya alcanza el RMSE del OLS crudo pero la
prediccion del modelo no, el problema esta aguas abajo (pooling / FiLM /
cabeza / optimizacion); si la sonda tambien cae, esta aguas arriba.

Las sondas se ajustan sobre ventanas de TRAIN y se evaluan sobre las
ventanas de VALIDATION cacheadas (mismos conjuntos para todas).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, torch
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SITES, load_model, predict_norm, metrics, td_anom_stats, DEFAULT_SILVER_DIR

OUT = Path(__file__).resolve().parent / "out"
mean, std = td_anom_stats()
ncells = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / "department_grid_ids" / f"{s}.csv")) for s in SITES}
tot = sum(ncells.values())

rng = np.random.default_rng(4242)
def take(split, n):
    d = dict(np.load(OUT / f"sample_{split}.npz")); d["site"] = d["site"].astype(str)
    i = rng.permutation(len(d["label"]))[:n]
    return {k: v[i] for k, v in d.items()}
tr, va = take("train", 80000), take("validation", 120000)
print(f"sonda: fit sobre {len(tr['label'])} ventanas de train, evaluacion sobre {len(va['label'])} de validation")

model = load_model("last.pt")

@torch.no_grad()
def feats(s, bs=4096):
    outs = {"h": [], "pooled": [], "mod": []}
    for i in range(0, len(s["label"]), bs):
        dyn = torch.from_numpy(s["dynamic"][i:i+bs]); sta = torch.from_numpy(s["static"][i:i+bs])
        reg = torch.from_numpy(s["region"][i:i+bs])
        h = model.tcn(model.input_proj(dyn))
        pooled = model.attention_pool(h)
        gamma, beta = model.film(sta, reg)
        outs["h"].append(h.reshape(len(dyn), -1).numpy())
        outs["pooled"].append(pooled.numpy())
        outs["mod"].append((gamma * pooled + beta).numpy())
    return {k: np.concatenate(v) for k, v in outs.items()}

ftr, fva = feats(tr), feats(va)

def site_extra(s):
    n = len(s["label"]); reg = np.zeros((n, 3), np.float32); reg[np.arange(n), s["region"]] = 1
    return np.concatenate([s["static"], reg[:, 1:], s["target_cond"]], 1)

def fit_eval(name, Xtr, ytr, Xva, s_va, ridge=1e-3):
    Xtr = np.concatenate([np.ones((len(Xtr), 1), np.float32), Xtr], 1).astype(np.float64)
    Xva = np.concatenate([np.ones((len(Xva), 1), np.float32), Xva], 1).astype(np.float64)
    A = Xtr.T @ Xtr + ridge * np.eye(Xtr.shape[1])
    b = Xtr.T @ ytr.astype(np.float64)
    w = np.linalg.solve(A, b)
    pn = Xva @ w
    obs = s_va["label"] * std + mean + s_va["td_clim"]
    phys = pn * std + mean + s_va["td_clim"]
    per = {s: metrics(phys[s_va["site"] == s], obs[s_va["site"] == s])["rmse"] for s in SITES}
    all_w = float(np.sqrt(sum(ncells[s] / tot * per[s] ** 2 for s in SITES)))
    return {"sonda": name, "n_feat": Xtr.shape[1], **{f"rmse_{s}": per[s] for s in SITES},
            "rmse_ALL_repond": all_w}

rows = []
rows.append(fit_eval("P0 entradas crudas (dynamic aplanado+static+region+target_cond)",
                     np.concatenate([tr["dynamic"].reshape(len(tr["label"]), -1), site_extra(tr)], 1),
                     tr["label"], np.concatenate([va["dynamic"].reshape(len(va["label"]), -1), site_extra(va)], 1), va))
rows.append(fit_eval("P1 salida del TCN aplanada (31x64) + static+region+target_cond",
                     np.concatenate([ftr["h"], site_extra(tr)], 1), tr["label"],
                     np.concatenate([fva["h"], site_extra(va)], 1), va))
rows.append(fit_eval("P2 pooled tras atencion (64) + static+region+target_cond",
                     np.concatenate([ftr["pooled"], site_extra(tr)], 1), tr["label"],
                     np.concatenate([fva["pooled"], site_extra(va)], 1), va))
rows.append(fit_eval("P3 entrada exacta de la cabeza: FiLM(pooled) (64) + target_cond",
                     np.concatenate([ftr["mod"], tr["target_cond"]], 1), tr["label"],
                     np.concatenate([fva["mod"], va["target_cond"]], 1), va))
rows.append(fit_eval("P4 solo target_cond + static + region (sin ventana)",
                     site_extra(tr), tr["label"], site_extra(va), va))

# la prediccion real del modelo sobre las mismas ventanas
pn = predict_norm(model, va)
obs = va["label"] * std + mean + va["td_clim"]
phys = pn * std + mean + va["td_clim"]
per = {s: metrics(phys[va["site"] == s], obs[va["site"] == s])["rmse"] for s in SITES}
rows.append({"sonda": "modelo entrenado (cabeza real, last.pt)", "n_feat": np.nan,
             **{f"rmse_{s}": per[s] for s in SITES},
             "rmse_ALL_repond": float(np.sqrt(sum(ncells[s]/tot*per[s]**2 for s in SITES)))})
pers = va["dynamic"][:, -1, 2]
physp = pers * std + mean + va["td_clim"]
perp = {s: metrics(physp[va["site"] == s], obs[va["site"] == s])["rmse"] for s in SITES}
rows.append({"sonda": "persistencia (TD_anom_norm en t)", "n_feat": np.nan,
             **{f"rmse_{s}": perp[s] for s in SITES},
             "rmse_ALL_repond": float(np.sqrt(sum(ncells[s]/tot*perp[s]**2 for s in SITES)))})

df = pd.DataFrame(rows)
pd.set_option("display.width", 240, "display.max_columns", 20, "display.float_format", lambda v: f"{v:.4f}")
print("\n=== RMSE (degC) de sondas lineales sobre representaciones internas ===")
print(df.to_string(index=False))
df.to_csv(OUT / "probes.csv", index=False)
