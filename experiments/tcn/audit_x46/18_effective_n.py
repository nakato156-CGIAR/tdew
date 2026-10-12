"""Cuantas observaciones independientes hay realmente por sitio.

El entrenamiento trata 1.740 millones de ventanas como muestras
independientes. Se mide el rango efectivo espacial de cada sitio a partir
del espectro de la matriz de correlacion entre celdas (serie TD_anom_norm
completa 2002-2016), y se compara con el numero de celdas declarado.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SITES, make_dataset

ds = make_dataset("train")
b = ds._load_bucket(0)
site_of = ds._site_of_id
ids_by_site = {s: [] for s in SITES}
for i in b["id_ranges"]:
    s = site_of.get(int(i))
    if s: ids_by_site[s].append(int(i))

rng = np.random.default_rng(11)
rows = []
for s in SITES:
    pool = np.array(ids_by_site[s])
    k = min(300, len(pool))
    pick = rng.choice(pool, size=k, replace=False)
    ser = []
    for i in pick:
        a, e = b["id_ranges"][int(i)]
        ser.append(b["label_arr"][a:e])
    L = min(len(v) for v in ser)
    M = np.stack([v[:L] for v in ser]).astype(np.float64)
    M = (M - M.mean(1, keepdims=True)) / M.std(1, keepdims=True)
    C = (M @ M.T) / M.shape[1]
    ev = np.sort(np.linalg.eigvalsh(C))[::-1]
    ev = np.clip(ev, 0, None)
    cum = np.cumsum(ev) / ev.sum()
    pr = float(ev.sum() ** 2 / (ev ** 2).sum())   # participation ratio
    off = C[np.triu_indices(k, 1)]
    rows.append({"sitio": s, "celdas_muestreadas": k, "dias": L,
                 "corr_mediana_entre_celdas": float(np.median(off)),
                 "var_1er_componente": float(ev[0] / ev.sum()),
                 "comp_para_90pct": int(np.searchsorted(cum, 0.90) + 1),
                 "comp_para_99pct": int(np.searchsorted(cum, 0.99) + 1),
                 "rango_efectivo_PR": pr})
d = pd.DataFrame(rows)
pd.set_option("display.width", 220, "display.float_format", lambda v: f"{v:.4f}")
print("espectro de la correlacion entre celdas (bucket 0, serie completa)\n")
print(d.to_string(index=False))

print("\n=== combinado con el tamano real de cada sitio ===")
from common import DEFAULT_SILVER_DIR
nc = {s: len(pd.read_csv(DEFAULT_SILVER_DIR / f"department_grid_ids/{s}.csv")) for s in SITES}
import json
sw = json.loads((Path(__file__).resolve().parents[1] / "experiments/tcn/site_weights.json").read_text())
for _, r in d.iterrows():
    s = r.sitio
    frac = r.rango_efectivo_PR / r.celdas_muestreadas
    print(f"   {s:22s} celdas={nc[s]:>7,}  ventanas_train={sw['train_n_eligible_targets'][s]:>13,}  "
          f"rango_efectivo/celdas={frac:.4f}  -> celdas efectivas ~ {nc[s]*frac:,.0f}")
