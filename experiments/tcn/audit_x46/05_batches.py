"""Mide los batches REALES que entrega el DataLoader de entrenamiento
(no deducidos del codigo) y, por separado, reconstruye con el indice de
secuencias real la composicion por sitio a lo largo de un bucket completo.
"""
import sys, time, json
from pathlib import Path
import numpy as np, pandas as pd, torch
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ROOT, SITES, make_dataset, DYNAMIC_COLS, DEFAULT_GOLD_DIR,
                    SITE_WEIGHTS_PATH, td_anom_stats)
from experiments.tcn.train import build_dataloader
from experiments.tcn.dataset import load_site_weights, DEFAULT_SILVER_DIR

OUT = Path(__file__).resolve().parent / "out"
sw = load_site_weights(SITE_WEIGHTS_PATH)
w2site = {round(float(v), 18): k for k, v in sw.items()}
print("pesos por sitio (experiments/tcn/site_weights.json):", sw)

N_BATCHES = 120
ds, loader = build_dataloader(
    gold_dir=DEFAULT_GOLD_DIR, silver_dir=DEFAULT_SILVER_DIR, context_length=31,
    split="train", site_weights=sw, batch_size=1024, num_workers=2, seed=0, max_buckets=None)
ds.set_epoch(0)

rows, t0 = [], time.time()
first_batch = None
for i, b in enumerate(loader):
    if i >= N_BATCHES:
        break
    if first_batch is None:
        first_batch = {k: v.clone() for k, v in b.items()}
    w = b["weight"].numpy()
    counts = {s: int((np.isclose(w, np.float32(sw[s]), rtol=1e-6, atol=0.0)).sum()) for s in SITES}
    share = {s: counts[s] * sw[s] for s in SITES}
    tot = sum(share.values())
    rows.append({"batch": i, "n": len(w),
                 **{f"n_{s}": counts[s] for s in SITES},
                 **{f"grad_share_{s}": share[s] / tot for s in SITES},
                 "ess": float(w.sum() ** 2 / (w ** 2).sum()),
                 "n_ids_unicos": int(len(np.unique(b["id"].numpy()))),
                 "label_std": float(b["label"].std()),
                 "nan_dyn": int(torch.isnan(b["dynamic"]).sum()),
                 "nan_label": int(torch.isnan(b["label"]).sum())})
el = time.time() - t0
df = pd.DataFrame(rows)
print(f"\n{N_BATCHES} batches reales en {el:.1f}s ({N_BATCHES/el:.2f} batches/s, "
      f"{N_BATCHES*1024/el:,.0f} muestras/s) con num_workers=2")
pd.set_option("display.width", 250, "display.max_columns", 40, "display.float_format", lambda v: f"{v:.4f}")
print("\n=== resumen sobre los 150 batches ===")
print(df.drop(columns=["batch"]).describe().loc[["mean", "min", "max"]].to_string())
print("\n=== primeros 5 y ultimos 5 batches ===")
print(pd.concat([df.head(5), df.tail(5)]).to_string(index=False))
df.to_csv(OUT / "batches.csv", index=False)

print("\n=== contenido del primer batch ===")
for k, v in first_batch.items():
    print(f"   {k:16s} {tuple(v.shape)} {v.dtype}")
d = first_batch["dynamic"].numpy()
for j, c in enumerate(DYNAMIC_COLS):
    print(f"   dynamic[:,:,{j}] {c:16s} mean={d[:,:,j].mean():+.4f} std={d[:,:,j].std():.4f} "
          f"min={d[:,:,j].min():+.3f} max={d[:,:,j].max():+.3f}")
lab = first_batch["label"].numpy()
td_t = d[:, -1, DYNAMIC_COLS.index("TD_anom_norm")]
print(f"   corr(label, TD_anom_norm(t)) = {np.corrcoef(lab, td_t)[0,1]:.5f}")
print(f"   label mean={lab.mean():+.4f} std={lab.std():.4f}")
print(f"   fechas distintas en el batch = {len(np.unique(first_batch['date_ordinal'].numpy()))}")

# ---- composicion por sitio a lo largo de UN bucket completo, desde el indice real
print("\n=== emision por sitio dentro de un bucket completo (indice real L=31, split train) ===")
seq = pd.read_parquet(DEFAULT_GOLD_DIR / "sequence_index/L=31/id_bucket=0/part.parquet")
seq = seq[(seq.split == "train") & (seq.n_eligible_targets > 0)]
seq["_site"] = seq["ID"].map(ds._site_of_id)
seq = seq[seq["_site"].notna()]
per_site = seq.groupby("_site")["n_eligible_targets"].agg(["size", "sum"])
per_site.columns = ["celdas_en_bucket", "muestras_en_bucket"]
print(per_site.to_string())
# round-robin exacto: cada sitio aporta 1 por ronda mientras le queden muestras
tot_site = per_site["muestras_en_bucket"].to_dict()
order = sorted(tot_site.items(), key=lambda kv: kv[1])
emitted, rounds_done, alive = {s: 0 for s in tot_site}, 0, dict(tot_site)
cum = []
for s, n in order:
    delta = n - rounds_done
    rounds_done = n
    cum.append((s, rounds_done, dict(alive)))
    alive.pop(s)
pos = 0
print("\n  fases del round-robin (posicion acumulada en muestras del bucket):")
prev = 0
alive = set(tot_site)
for s, r, _ in cum:
    k = len(alive)
    emitted_here = (r - prev) * k
    pos += emitted_here
    print(f"   hasta ronda {r:>10,}: {k} sitios vivos ({', '.join(sorted(alive))}) "
          f"-> {emitted_here:>12,} muestras acumulando hasta {pos:>12,}")
    prev = r
    alive.discard(s)
total_bucket = sum(tot_site.values())
print(f"   total del bucket = {total_bucket:,} muestras")

# --- correlacion intra-batch: cuantas muestras efectivamente independientes hay ---
print("\n=== dependencia dentro de un batch real ===")
ids = first_batch["id"].numpy()
u, c = np.unique(ids, return_counts=True)
print(f"   celdas distintas en el batch: {len(u)} (batch de {len(ids)})")
print(f"   muestras por celda: min={c.min()} mediana={int(np.median(c))} max={c.max()}")
lab = first_batch["label"].numpy()
between = np.array([lab[ids == i].mean() for i in u])
ss_between = float(sum(((lab[ids == i].mean() - lab.mean()) ** 2).sum() * (ids == i).sum() for i in u))
ss_tot = float(((lab - lab.mean()) ** 2).sum())
print(f"   fraccion de la varianza del label explicada por la celda = {ss_between/ss_tot:.4f}")
