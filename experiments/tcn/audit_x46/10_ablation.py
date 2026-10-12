"""Experimento controlado pequeno (CPU) para separar arquitectura de datos.

Cuatro variantes entrenadas con EXACTAMENTE los mismos batches, la misma
perdida, el mismo optimizador, la misma semilla y el mismo numero de pasos,
sobre la submuestra de train cacheada, evaluadas sobre la submuestra de
validation cacheada:

  A  arquitectura actual (tdew_estimation.models.TCNAttentionModel)
  B  A con FiLM en identidad: (1+gamma)*h + beta en vez de gamma*h + beta
  C  A con conexion residual de persistencia: pred = TD_anom_norm(t) + salida
  D  B + C
  E  A con pesos por sitio uniformes (aisla el efecto de la ponderacion)

No sustituye al entrenamiento real (1.700.000 pasos/epoca sobre 436.519
celdas); es una comparacion relativa bajo condiciones identicas.
"""
import sys, time, copy
from pathlib import Path
import numpy as np, pandas as pd, torch
import torch.nn.functional as F
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, metrics, td_anom_stats, DEFAULT_SILVER_DIR, DYNAMIC_COLS,
                    SITE_WEIGHTS_PATH)
from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel
from tdew_estimation.models.conditioning import FiLMGenerator
from experiments.tcn.dataset import load_site_weights

OUT = Path(__file__).resolve().parent / "out"
mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
ncells = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / "department_grid_ids" / f"{s}.csv")) for s in SITES}
tot = sum(ncells.values())
sw = load_site_weights(SITE_WEIGHTS_PATH)

rng = np.random.default_rng(2026)
tr = dict(np.load(OUT / "sample_train.npz")); tr["site"] = tr["site"].astype(str)
va = dict(np.load(OUT / "sample_validation.npz")); va["site"] = va["site"].astype(str)
iv = rng.permutation(len(va["label"]))[:60000]
va = {k: v[iv] for k, v in va.items()}
print(f"train={len(tr['label'])} ventanas, validation={len(va['label'])} ventanas")

T = {k: torch.from_numpy(tr[k]) for k in ["dynamic", "static", "region", "target_cond", "label", "weight"]}
V = {k: torch.from_numpy(va[k]) for k in ["dynamic", "static", "region", "target_cond"]}
obs_va = va["label"] * std + mean + va["td_clim"]

STEPS, BS, EVAL_EVERY = 1500, 512, 250
order_rng = np.random.default_rng(7)
batch_idx = [order_rng.integers(0, len(tr["label"]), BS) for _ in range(STEPS)]


class Wrap(torch.nn.Module):
    def __init__(self, film_identity: bool, residual: bool, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.m = TCNAttentionModel(TCNAttentionConfig())
        self.film_identity, self.residual = film_identity, residual

    def forward(self, dyn, sta, reg, tc):
        m = self.m
        h = m.tcn(m.input_proj(dyn))
        pooled = m.attention_pool(h)
        gamma, beta = m.film(sta, reg)
        if self.film_identity:
            gamma = gamma + 1.0
        pooled = gamma * pooled + beta
        out = m.head(torch.cat([pooled, tc], -1)).squeeze(-1)
        if self.residual:
            out = out + dyn[:, -1, TD_IDX]
        return out


@torch.no_grad()
def eval_rmse(model):
    model.eval()
    ps = []
    for i in range(0, len(va["label"]), 8192):
        ps.append(model(V["dynamic"][i:i+8192], V["static"][i:i+8192],
                        V["region"][i:i+8192], V["target_cond"][i:i+8192]).numpy())
    pn = np.concatenate(ps)
    phys = pn * std + mean + va["td_clim"]
    per = {s: metrics(phys[va["site"] == s], obs_va[va["site"] == s])["rmse"] for s in SITES}
    model.train()
    return float(np.sqrt(sum(ncells[s] / tot * per[s] ** 2 for s in SITES))), per


print("\n=== norma del gradiente que llega a input_proj en el paso 0 ===")
for name, fi in [("A gamma*h+beta", False), ("B (1+gamma)*h+beta", True)]:
    mdl = Wrap(fi, False, seed=0)
    i = batch_idx[0]
    p = mdl(T["dynamic"][i], T["static"][i], T["region"][i], T["target_cond"][i])
    l = (F.huber_loss(p, T["label"][i], delta=1.0, reduction="none") * T["weight"][i]).sum() / T["weight"][i].sum()
    l.backward()
    gi = mdl.m.input_proj.weight.grad.norm().item()
    gh = mdl.m.head[0].weight.grad.norm().item()
    print(f"   {name:22s} ||grad input_proj||={gi:.3e}  ||grad head.0||={gh:.3e}  razon={gi/gh:.4f}")

rows = []
for name, fi, res, uni in [("A actual", False, False, False),
                           ("B FiLM identidad", True, False, False),
                           ("C residual persistencia", False, True, False),
                           ("D B+C", True, True, False),
                           ("E actual, pesos uniformes", False, False, True)]:
    t0 = time.time()
    model = Wrap(fi, res, seed=0)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4)
    hist = []
    for k, i in enumerate(batch_idx):
        opt.zero_grad(set_to_none=True)
        p = model(T["dynamic"][i], T["static"][i], T["region"][i], T["target_cond"][i])
        per_s = F.huber_loss(p, T["label"][i], delta=1.0, reduction="none")
        w = torch.ones_like(per_s) if uni else T["weight"][i]
        loss = (per_s * w).sum() / w.sum()
        loss.backward(); opt.step()
        if (k + 1) % EVAL_EVERY == 0:
            r, per = eval_rmse(model)
            hist.append((k + 1, float(loss), r))
    r, per = eval_rmse(model)
    rows.append({"variante": name, "rmse_ALL_repond": r, **{f"rmse_{s}": per[s] for s in SITES},
                 "segundos": time.time() - t0})
    print(f"\n{name}: {[(k, round(l,5), round(rr,4)) for k, l, rr in hist]}  ({time.time()-t0:.0f}s)")

df = pd.DataFrame(rows)
pd.set_option("display.width", 220, "display.float_format", lambda v: f"{v:.4f}")
print("\n=== tras 1500 pasos identicos (batch 512) ===")
print(df.to_string(index=False))
df.to_csv(OUT / "ablation.csv", index=False)
