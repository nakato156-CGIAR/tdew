"""El train_loss registrado en MLflow (0.0437-0.0482) no coincide con la
perdida que produce el propio modelo entrenado. Se comprueba (a) cuanto vale
realmente la perdida ponderada sobre train, y (b) si el calculo en bfloat16
que usa el entrenamiento (autocast en GPU) la distorsiona.

Tambien se miden dos cosas que faltaban: la correlacion del label con la
persistencia cruda en el mismo subconjunto, y cuanto aporta target_cond en un
ajuste lineal.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, torch
import torch.nn.functional as F
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, DEFAULT_SILVER_DIR, SITE_WEIGHTS_PATH)
from tdew_estimation.models.losses import weighted_huber_loss
from experiments.tcn.dataset import load_site_weights

OUT = Path(__file__).resolve().parent / "out"
mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
sw = load_site_weights(SITE_WEIGHTS_PATH)
ncells = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / f"department_grid_ids/{s}.csv")) for s in SITES}
tot = sum(ncells.values())

tr = dict(np.load(OUT / "sample_train.npz")); tr["site"] = tr["site"].astype(str)
va = dict(np.load(OUT / "sample_validation.npz")); va["site"] = va["site"].astype(str)
model = load_model("last.pt")

print("=== A. perdida real del modelo entrenado sobre TRAIN ===")
rng = np.random.default_rng(5)
i = rng.permutation(len(tr["label"]))[:120000]
sub = {k: v[i] for k, v in tr.items()}
p = torch.from_numpy(predict_norm(model, sub))
y = torch.from_numpy(sub["label"]); w = torch.from_numpy(sub["weight"])
print(f"   Huber ponderado (float32)     = {float(weighted_huber_loss(p, y, w, 1.0)):.6f}")
print(f"   Huber sin ponderar (float32)  = {float(F.huber_loss(p, y, delta=1.0)):.6f}")
obs = sub["label"] * std + mean + sub["td_clim"]
phys = sub["label"] * 0 + predict_norm(model, sub) * std + mean + sub["td_clim"]
per = {s: metrics(phys[sub["site"] == s], obs[sub["site"] == s])["rmse"] for s in SITES}
print(f"   RMSE train por sitio: " + "  ".join(f"{s}={per[s]:.4f}" for s in SITES))
print(f"   train_loss registrado en MLflow, epoca 4 = 0.043734 (ver audit/01_mlflow_dump.py)")

print("\n=== B. el mismo calculo en bfloat16, como en el entrenamiento (autocast) ===")
for bs in [1024]:
    rows = []
    for k in range(0, 60 * bs, bs):
        pp, yy, ww = p[k:k+bs], y[k:k+bs], w[k:k+bs]
        f32 = float(weighted_huber_loss(pp, yy, ww, 1.0))
        b16 = float(weighted_huber_loss(pp.bfloat16(), yy.bfloat16(), ww.bfloat16(), 1.0))
        # desglose del numerador/denominador
        ps16 = F.huber_loss(pp.bfloat16(), yy.bfloat16(), delta=1.0, reduction="none")
        num16 = float((ps16 * ww.bfloat16()).sum()); den16 = float(ww.bfloat16().sum())
        num32 = float((F.huber_loss(pp, yy, delta=1.0, reduction="none") * ww).sum()); den32 = float(ww.sum())
        rows.append({"float32": f32, "bfloat16": b16, "razon": b16 / f32,
                     "num_b16/num_f32": num16 / num32, "den_b16/den_f32": den16 / den32})
    d = pd.DataFrame(rows)
    pd.set_option("display.float_format", lambda v: f"{v:.6f}")
    print(f"   batch={bs}, {len(d)} batches:")
    print(d.describe().loc[["mean", "min", "max"]].to_string())

print("\n   mismo experimento con pesos uniformes (=1) para aislar el efecto de la escala de w:")
w1 = torch.ones_like(w)
f32 = float(weighted_huber_loss(p[:1024], y[:1024], w1[:1024], 1.0))
b16 = float(weighted_huber_loss(p[:1024].bfloat16(), y[:1024].bfloat16(), w1[:1024].bfloat16(), 1.0))
print(f"   float32={f32:.6f}  bfloat16={b16:.6f}  razon={b16/f32:.4f}")

print("\n=== C. escala del gradiente: d(loss)/d(pred) en float32 vs bfloat16 ===")
for dt in [torch.float32, torch.bfloat16]:
    pp = p[:1024].clone().to(dt).requires_grad_(True)
    l = weighted_huber_loss(pp, y[:1024].to(dt), w[:1024].to(dt), 1.0)
    l.backward()
    print(f"   {str(dt):16s} loss={float(l):.6f}  ||grad||={float(pp.grad.float().norm()):.6e}")

print("\n=== D. correlaciones sobre el mismo subconjunto de validation ===")
rng = np.random.default_rng(1234)
iv = rng.permutation(len(va["label"]))[:60000]
s2 = {k: v[iv] for k, v in va.items()}
pn = predict_norm(model, s2)
print(f"   corr(label, TD_anom_norm(t))  [persistencia] = {np.corrcoef(s2['label'], s2['dynamic'][:,-1,TD_IDX])[0,1]:.5f}")
print(f"   corr(label, pred del modelo)                 = {np.corrcoef(s2['label'], pn)[0,1]:.5f}")
print(f"   std(label)={s2['label'].std():.4f}  std(TD(t))={s2['dynamic'][:,-1,TD_IDX].std():.4f}  std(pred)={pn.std():.4f}")

print("\n=== E. cuanto aporta target_cond (LST/doy del dia objetivo) a un lineal ===")
def ev(Xtr, ytr, Xva, name):
    Xtr = np.c_[np.ones(len(Xtr)), Xtr]; Xva = np.c_[np.ones(len(Xva)), Xva]
    w_ = np.linalg.lstsq(Xtr, ytr, rcond=None)[0]
    pnv = Xva @ w_
    o = va["label"] * std + mean + va["td_clim"]; ph = pnv * std + mean + va["td_clim"]
    per = {s: metrics(ph[va["site"] == s], o[va["site"] == s])["rmse"] for s in SITES}
    r = float(np.sqrt(sum(ncells[s]/tot*per[s]**2 for s in SITES)))
    print(f"   {name:52s} rmse_ALL_repond={r:.4f}  " + " ".join(f"{s[:4]}={per[s]:.4f}" for s in SITES))
    return r
def blocks(s, with_tc, ndays=31):
    n = len(s["label"]); reg = np.zeros((n, 3)); reg[np.arange(n), s["region"]] = 1
    parts = [s["dynamic"][:, -ndays:, :].reshape(n, -1), s["static"], reg[:, 1:]]
    if with_tc: parts.append(s["target_cond"])
    return np.concatenate([x.astype(np.float64) for x in parts], 1)
ytr = tr["label"].astype(np.float64)
ev(blocks(tr, True), ytr, blocks(va, True), "OLS 31 dias + static + region + target_cond")
ev(blocks(tr, False), ytr, blocks(va, False), "OLS 31 dias + static + region (sin target_cond)")
ev(blocks(tr, True, 3), ytr, blocks(va, True, 3), "OLS solo 3 dias + static + region + target_cond")
ev(blocks(tr, True, 1), ytr, blocks(va, True, 1), "OLS solo 1 dia + static + region + target_cond")
