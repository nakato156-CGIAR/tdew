"""Correspondencia entre la funcion objetivo optimizada (Huber ponderado por
sitio, delta=1, en unidades de TD_anom_norm) y la metrica con la que se
evalua y se selecciona el checkpoint (RMSE agrupado sin ponderar, en degC).

Todo se mide sobre los residuos REALES del modelo entrenado en la
submuestra de validation.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, torch
import torch.nn.functional as F
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    SITE_WEIGHTS_PATH, DEFAULT_SILVER_DIR)
from experiments.tcn.dataset import load_site_weights

OUT = Path(__file__).resolve().parent / "out"
val = dict(np.load(OUT / "sample_validation.npz"))
val["site"] = val["site"].astype(str)
mean, std = td_anom_stats()
sw = load_site_weights(SITE_WEIGHTS_PATH)
ncells = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / "department_grid_ids" / f"{s}.csv")) for s in SITES}
tot_cells = sum(ncells.values())

rng = np.random.default_rng(99)
idx = rng.permutation(len(val["label"]))[:120000]
sub = {k: v[idx] for k, v in val.items()}
model = load_model("last.pt")
pred = predict_norm(model, sub)
res = pred - sub["label"]          # residuo en unidades normalizadas
res_phys = res * std              # residuo en degC

print(f"n={len(res)} ventanas de validation (submuestra balanceada por sitio)")
print(f"std de TD_anom = {std:.6f} degC por unidad normalizada\n")

print("=== 1. regimen de Huber(delta=1) sobre los residuos reales ===")
for d in [1.0]:
    frac = float((np.abs(res) > d).mean())
    print(f"   fraccion de residuos con |r| > delta={d}: {frac:.4%}")
    hub = F.huber_loss(torch.tensor(pred), torch.tensor(sub['label']), delta=d, reduction='none').numpy()
    quad = 0.5 * res ** 2
    print(f"   masa de perdida en el tramo lineal: {float(hub[np.abs(res)>d].sum()/hub.sum()):.4%}")
    print(f"   masa de error cuadratico en esos mismos residuos: {float((res[np.abs(res)>d]**2).sum()/(res**2).sum()):.4%}")
print("   -> la parte de la distribucion que mas pesa en RMSE es la que Huber atenua")

print("\n=== 2. ponderacion por sitio: lo que optimiza la perdida vs lo que mide RMSE ===")
rows = []
for s in SITES:
    m = sub["site"] == s
    rows.append({"sitio": s, "n_submuestra": int(m.sum()),
                 "peso_por_muestra": sw[s],
                 "rmse_degC": float(np.sqrt(np.mean(res_phys[m] ** 2))),
                 "mse_norm": float(np.mean(res[m] ** 2)),
                 "share_celdas_reales": ncells[s] / tot_cells})
d = pd.DataFrame(rows)
# share del gradiente que recibe cada sitio en un batch round-robin equilibrado
d["share_grad_batch_equilibrado"] = d["peso_por_muestra"] / d["peso_por_muestra"].sum()
# share que recibiria si el batch siguiera la frecuencia natural (intencion declarada 1/n)
d["share_grad_si_frec_natural"] = (d["peso_por_muestra"] * d["share_celdas_reales"])
d["share_grad_si_frec_natural"] /= d["share_grad_si_frec_natural"].sum()
pd.set_option("display.width", 220, "display.float_format", lambda v: f"{v:.6g}")
print(d.to_string(index=False))
print(f"\n   razon max/min del share de gradiente en batch equilibrado: "
      f"{d['share_grad_batch_equilibrado'].max()/d['share_grad_batch_equilibrado'].min():.2f}")

print("\n=== 3. RMSE agrupado: submuestra balanceada vs poblacion real ===")
mse_bal = float(np.mean([r["mse_norm"] for r in rows])) * std ** 2
mse_pop = float(sum(ncells[r["sitio"]] / tot_cells * r["mse_norm"] for r in rows)) * std ** 2
print(f"   RMSE ALL con 25%/sitio          = {np.sqrt(mse_bal):.4f} degC")
print(f"   RMSE ALL con celdas reales      = {np.sqrt(mse_pop):.4f} degC")
print(f"   (Loreto pesa {ncells['iquitos_loreto']/tot_cells:.1%} de las celdas)")

print("\n=== 4. el objetivo ponderado vs el RMSE: signo de la discrepancia ===")
w = np.array([sw[s] for s in sub["site"]])
loss_w = float((F.huber_loss(torch.tensor(pred), torch.tensor(sub['label']), delta=1.0, reduction='none').numpy() * w).sum() / w.sum())
loss_u = float(F.huber_loss(torch.tensor(pred), torch.tensor(sub['label']), delta=1.0).item())
print(f"   Huber ponderado (lo que se minimiza)   = {loss_w:.6f}")
print(f"   Huber sin ponderar                     = {loss_u:.6f}")
print(f"   0.5*MSE sin ponderar (norm)            = {0.5*float(np.mean(res**2)):.6f}")
print(f"   train_loss registrado en MLflow es de este orden -> ver 01_mlflow_dump")
