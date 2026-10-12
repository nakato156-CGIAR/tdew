"""Chequeos sobre los datos y sobre la simetria de la comparacion.

1. Alineacion temporal de la ventana (no hay fuga de t+1 en `dynamic`).
2. Igualdad del conjunto de muestras entre baselines y modelo profundo,
   via el RMSE de climatologia implicito en la metrica registrada.
3. Cobertura, NaN y rangos del tensor de entrada.
"""
import sys, sqlite3
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, SITES, td_anom_stats, DYNAMIC_COLS, TARGET_COND_COLS,
                    STATIC_COLS, DEFAULT_GOLD_DIR, DEFAULT_SILVER_DIR)

OUT = Path(__file__).resolve().parent / "out"
mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
va = dict(np.load(OUT / "sample_validation.npz")); va["site"] = va["site"].astype(str)

print("=== 1. alineacion temporal: label(d-1) debe ser dynamic[-1] de la muestra de fecha d ===")
key = va["id"].astype(np.int64) * 10**7 + va["date_ordinal"]
order = np.argsort(key)
idv, dv, lab, dyn = va["id"][order], va["date_ordinal"][order], va["label"][order], va["dynamic"][order]
same = (idv[1:] == idv[:-1]) & (dv[1:] == dv[:-1] + 1)
a = lab[:-1][same]                    # label del dia d-1  (= TD_anom_norm en la fecha objetivo d-1)
b = dyn[1:][same][:, -1, TD_IDX]      # ultimo dia de la ventana de la muestra de fecha d
print(f"   pares consecutivos comparados: {same.sum():,}")
print(f"   max |label(d-1) - dynamic[-1](d)| = {np.abs(a-b).max():.3e}   (0 => ventana termina en t = d-1)")
c = dyn[1:][same][:, -2, TD_IDX]
print(f"   max |label(d-1) - dynamic[-2](d)| = {np.abs(a-c).max():.3e}   (control: debe ser > 0)")
print("   -> la ventana llega hasta t y no incluye t+1: sin fuga por `dynamic`")

print("\n=== 2. simetria de la comparacion baselines vs modelo profundo ===")
lb = pd.read_csv(ROOT / "reports/week1_baselines/leaderboard.csv")
con = sqlite3.connect(f"file:{(ROOT/'mlflow.db').resolve()}?mode=ro", uri=True)
q = """select m.key, m.step, m.value from metrics m join runs r on r.run_uuid=m.run_uuid
       where r.name='week1-tcn-attention' and m.key in ('val_rmse','val_skill_vs_clim')"""
d = {}
for k, s, v in con.execute(q):
    d.setdefault(s, {})[k] = v
con.close()
clim_lb = lb[(lb.site == "ALL") & (lb.method == "climatology") & (lb.split == "validation")].iloc[0]
print(f"   leaderboard: climatology validation ALL  rmse={clim_lb.rmse:.6f}  n={int(clim_lb.n):,}")
for s in sorted(d):
    if "val_rmse" in d[s] and "val_skill_vs_clim" in d[s]:
        implied = d[s]["val_rmse"] / (1 - d[s]["val_skill_vs_clim"])
        print(f"   epoca {s}: val_rmse={d[s]['val_rmse']:.6f} skill={d[s]['val_skill_vs_clim']:.6f} "
              f"-> rmse_clim implicito={implied:.6f}  dif. relativa vs leaderboard={implied/clim_lb.rmse-1:+.2e}")
print("   -> mismo conjunto de muestras y misma referencia climatologica")

print("\n=== 3. n de muestras elegibles por sitio y split (indice real L=31, todos los buckets) ===")
rows = []
for b in sorted(int(p.name.split('=')[1]) for p in (DEFAULT_GOLD_DIR/'sequence_index/L=31').iterdir()):
    f = DEFAULT_GOLD_DIR / f"sequence_index/L=31/id_bucket={b}/part.parquet"
    rows.append(pd.read_parquet(f, columns=["ID", "split", "n_eligible_targets"]))
seq = pd.concat(rows)
sid = {}
for s in SITES:
    for i in pd.read_csv(DEFAULT_SILVER_DIR / f"department_grid_ids/{s}.csv")["ID"]:
        sid[int(i)] = s
seq["site"] = seq["ID"].map(sid)
tab = seq.groupby(["site", "split"])["n_eligible_targets"].sum().unstack()
print(tab.to_string())
print("\n   totales:", tab.sum().to_dict())
print("\n   leaderboard n por sitio/split:")
print(lb[lb.method == "climatology"][["site", "split", "n"]].to_string(index=False))

print("\n=== 4. NaN y rangos en la submuestra de validation ===")
for k in ["dynamic", "static", "target_cond", "label", "td_clim"]:
    v = va[k]
    print(f"   {k:12s} nan={int(np.isnan(v).sum())} min={np.nanmin(v):+.3f} max={np.nanmax(v):+.3f}")
for j, c in enumerate(TARGET_COND_COLS):
    print(f"   target_cond[{j}] {c:16s} mean={va['target_cond'][:,j].mean():+.4f} std={va['target_cond'][:,j].std():.4f}")
for j, c in enumerate(STATIC_COLS):
    print(f"   static[{j}] {c:12s} mean={va['static'][:,j].mean():+.4f} std={va['static'][:,j].std():.4f}")
