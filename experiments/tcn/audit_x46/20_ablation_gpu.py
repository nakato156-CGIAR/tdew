"""Version ampliada del experimento controlado de audit/10_ablation.py, en
GPU: 640 celdas por sitio-conjunto (8 buckets x 20 celdas/sitio, 2,55 M
ventanas de train) y 20.000 pasos a batch 1024, frente a las 128 celdas y
1.500 pasos de la version en CPU.

Pregunta que responde: (a) si la arquitectura actual es capaz de llegar al
nivel de los baselines con un presupuesto de pasos pequeno, y (b) si al
seguir entrenando la RMSE de validation se degrada, como ocurre en el run
de produccion.

Se evalua siempre sobre las MISMAS 559.200 ventanas de validation cacheadas,
agregadas a 'ALL' reponderando por el numero real de celdas por sitio.
"""
import sys, time
from pathlib import Path
import numpy as np, pandas as pd, torch
import torch.nn.functional as F
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SITES, metrics, td_anom_stats, DEFAULT_SILVER_DIR, DYNAMIC_COLS, SITE_WEIGHTS_PATH
from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel
from experiments.tcn.dataset import load_site_weights

OUT = Path(__file__).resolve().parent / "out"
dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("dispositivo:", dev, torch.cuda.get_device_name(0) if dev.type == "cuda" else "")
mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
ncells = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / f"department_grid_ids/{s}.csv")) for s in SITES}
tot = sum(ncells.values())

tr = dict(np.load(OUT / "sample_train_big.npz")); tr["site"] = tr["site"].astype(str)
va = dict(np.load(OUT / "sample_validation.npz")); va["site"] = va["site"].astype(str)
print(f"train={len(tr['label']):,} ventanas ({len(np.unique(tr['id']))} celdas), "
      f"validation={len(va['label']):,} ventanas ({len(np.unique(va['id']))} celdas)")

T = {k: torch.from_numpy(tr[k]).to(dev) for k in ["dynamic","static","region","target_cond","label","weight"]}
V = {k: torch.from_numpy(va[k]).to(dev) for k in ["dynamic","static","region","target_cond"]}
obs = va["label"] * std + mean + va["td_clim"]
site_mask = {s: va["site"] == s for s in SITES}

STEPS, BS, EVAL_EVERY = 20000, 1024, 2000
g = torch.Generator(device=dev).manual_seed(7)

class Wrap(torch.nn.Module):
    def __init__(self, film_identity, residual, seed=0):
        super().__init__(); torch.manual_seed(seed)
        self.m = TCNAttentionModel(TCNAttentionConfig())
        self.fi, self.res = film_identity, residual
    def forward(self, dyn, sta, reg, tc):
        m = self.m
        pooled = m.attention_pool(m.tcn(m.input_proj(dyn)))
        gamma, beta = m.film(sta, reg)
        if self.fi: gamma = gamma + 1.0
        out = m.head(torch.cat([gamma * pooled + beta, tc], -1)).squeeze(-1)
        return out + dyn[:, -1, TD_IDX] if self.res else out

@torch.no_grad()
def ev(model):
    model.eval(); ps = []
    for i in range(0, len(va["label"]), 32768):
        ps.append(model(V["dynamic"][i:i+32768], V["static"][i:i+32768],
                        V["region"][i:i+32768], V["target_cond"][i:i+32768]).float().cpu().numpy())
    pn = np.concatenate(ps); phys = pn * std + mean + va["td_clim"]
    per = {s: metrics(phys[site_mask[s]], obs[site_mask[s]])["rmse"] for s in SITES}
    model.train()
    return float(np.sqrt(sum(ncells[s]/tot*per[s]**2 for s in SITES))), per

rows, curves = [], {}
for name, fi, res, uni in [("A actual", False, False, False),
                           ("D FiLM identidad + residual persistencia", True, True, False),
                           ("E actual, pesos uniformes", False, False, True)]:
    torch.manual_seed(0)
    gg = torch.Generator(device=dev).manual_seed(7)   # mismo orden de batches para todas
    model = Wrap(fi, res, seed=0).to(dev)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)
    t0 = time.time(); c = []
    n = len(tr["label"])
    for k in range(STEPS):
        i = torch.randint(0, n, (BS,), generator=gg, device=dev)
        opt.zero_grad(set_to_none=True)
        p = model(T["dynamic"][i], T["static"][i], T["region"][i], T["target_cond"][i])
        ps_ = F.huber_loss(p, T["label"][i], delta=1.0, reduction="none")
        w = torch.ones_like(ps_) if uni else T["weight"][i]
        loss = (ps_ * w).sum() / w.sum()
        loss.backward(); opt.step()
        if (k + 1) % EVAL_EVERY == 0:
            r, _ = ev(model); c.append((k + 1, float(loss.item()), r))
    r, per = ev(model)
    curves[name] = c
    rows.append({"variante": name, "rmse_ALL_repond": r, **{f"rmse_{s}": per[s] for s in SITES},
                 "segundos": time.time() - t0})
    print(f"\n{name}  ({time.time()-t0:.0f}s)")
    for k, l, rr in c:
        print(f"    paso {k:>6,}  loss={l:.5f}  val_rmse_ALL={rr:.4f}")

d = pd.DataFrame(rows)
pd.set_option("display.width", 240, "display.float_format", lambda v: f"{v:.4f}")
print(f"\n=== tras {STEPS:,} pasos identicos (batch {BS}) sobre {len(tr['label']):,} ventanas ===")
print(d.to_string(index=False))
d.to_csv(OUT / "ablation_gpu.csv", index=False)
