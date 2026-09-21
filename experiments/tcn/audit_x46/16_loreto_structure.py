"""Dos mediciones sobre Loreto:
 (1) cuantas series distintas hay realmente entre las celdas (redundancia
     espacial del producto de origen);
 (2) RMSE del modelo y estadisticos libres de modelo, ano por ano, para
     distinguir un cambio en los datos de un ajuste especifico al periodo
     de entrenamiento.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, DEFAULT_GOLD_DIR, make_dataset)

mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
ds = make_dataset("train")
b = ds._load_bucket(0)
feat_ids = np.array(sorted(b["id_ranges"]))
site_of = ds._site_of_id
lor = np.array([i for i in feat_ids if site_of.get(i) == "iquitos_loreto"])
print(f"celdas de Loreto en el bucket 0: {len(lor)}")

print("\n=== 1. redundancia espacial: series TD_anom_norm identicas entre celdas ===")
rng = np.random.default_rng(3)
pick = rng.choice(lor, size=400, replace=False)
sers = {}
for i in pick:
    s0, e0 = b["id_ranges"][int(i)]
    sers[int(i)] = b["label_arr"][s0:e0]
L = min(len(v) for v in sers.values())
M = np.stack([v[:L] for v in sers.values()])
uniq = np.unique(M, axis=0)
print(f"   {len(M)} celdas muestreadas -> {len(uniq)} series distintas (longitud {L})")
# distancia tipica entre celdas distintas
sub = M[rng.choice(len(M), 60, replace=False)]
C = np.corrcoef(sub)
off = C[np.triu_indices(len(sub), 1)]
print(f"   correlacion entre pares de celdas distintas: mediana={np.median(off):.4f} "
      f"p10={np.quantile(off,0.1):.4f} p90={np.quantile(off,0.9):.4f} frac>0.999={float((off>0.999).mean()):.4f}")
# cuantas celdas comparten DEM/TDI/X/Y redondeados
stat = np.stack([b["static_mat"][b["id_ranges"][int(i)][0]] for i in pick])
print(f"   combinaciones (DEM,TDI,X,Y) distintas entre las {len(pick)} celdas: "
      f"{len(np.unique(np.round(stat,6), axis=0))}")

print("\n=== 2. por ano: RMSE del modelo vs predictores sin parametros (Loreto, bucket 0) ===")
model = load_model("last.pt")
rows = []
cells = rng.choice(lor, size=6, replace=False)
for split in ["train", "validation", "test"]:
    dss = make_dataset(split)
    bb = dss._load_bucket(0)
    seq = bb["seq"]
    seq = seq[seq["ID"].isin(cells.tolist())]
    samples = list(dss._samples_for_rows(bb, seq))
    if not samples:
        continue
    S = {k: np.stack([s[k] for s in samples]) for k in ["dynamic", "static", "region", "target_cond"]}
    lab = np.array([s["label"] for s in samples]); clim = np.array([s["td_clim_target"] for s in samples])
    dord = np.array([s["date_ordinal"] for s in samples])
    year = (np.datetime64("1970-01-01") + dord.astype("timedelta64[D]")).astype("datetime64[Y]").astype(int) + 1970
    pn = predict_norm(model, {**S, "label": lab})
    obs = lab * std + mean + clim
    for y in np.unique(year):
        k = year == y
        rows.append({"ano": int(y), "split": split, "n": int(k.sum()),
                     "std_label": float(lab[k].std()),
                     "rmse_modelo": metrics(pn[k]*std+mean+clim[k], obs[k])["rmse"],
                     "rmse_persist": metrics(S["dynamic"][k][:,-1,TD_IDX]*std+mean+clim[k], obs[k])["rmse"],
                     "rmse_clim": metrics(0*pn[k]+mean+clim[k], obs[k])["rmse"],
                     "autocorr1": float(np.corrcoef(lab[k], S["dynamic"][k][:,-1,TD_IDX])[0,1])})
d = pd.DataFrame(rows).sort_values("ano")
pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:.4f}")
print(d.to_string(index=False))
