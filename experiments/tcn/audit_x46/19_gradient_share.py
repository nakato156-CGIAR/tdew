"""Reparto real del gradiente por sitio a lo largo de una epoca.

La perdida es sum(w_i*h_i)/sum(w_i): dentro de un batch homogeneo en sitio
el peso se cancela por completo. Combinando eso con la composicion real que
produce el round-robin del dataset (calculada con el indice de secuencias
real), se obtiene la fraccion del gradiente de la epoca que recibe cada
sitio, y se compara con la intencion declarada (1/n_train_rows)."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import SITES, make_dataset, DEFAULT_GOLD_DIR

sw = json.loads((Path(__file__).resolve().parents[1] / "experiments/tcn/site_weights.json").read_text())
W = sw["weight"]; NTR = sw["train_n_eligible_targets"]
ds = make_dataset("train")
BS = 1024

tot = {s: 0.0 for s in SITES}; nb_tot = 0
buckets = sorted(int(p.name.split('=')[1]) for p in (DEFAULT_GOLD_DIR/'sequence_index/L=31').iterdir())
for b in buckets:
    seq = pd.read_parquet(DEFAULT_GOLD_DIR / f"sequence_index/L=31/id_bucket={b}/part.parquet",
                          columns=["ID", "split", "n_eligible_targets"])
    seq = seq[(seq.split == "train") & (seq.n_eligible_targets > 0)]
    seq["site"] = seq["ID"].map(ds._site_of_id)
    n = seq.groupby("site")["n_eligible_targets"].sum().to_dict()
    n = {s: float(n.get(s, 0.0)) for s in SITES}
    alive = {s: v for s, v in n.items() if v > 0}
    prev = 0.0
    while alive:
        r = min(alive.values())           # rondas hasta que se agota el siguiente sitio
        k = len(alive)
        rounds = r - prev
        n_batches = rounds * k / BS
        denom = sum(W[s] for s in alive)
        for s in alive:
            tot[s] += n_batches * (W[s] / denom)
        nb_tot += n_batches
        prev = r
        alive = {s: v for s, v in alive.items() if v > r}

d = pd.DataFrame([{"sitio": s,
                   "share_gradiente_epoca_real": tot[s] / nb_tot,
                   "share_si_todo_batch_equilibrado": W[s] / sum(W.values()),
                   "share_intencion_1_sobre_n": 0.25,
                   "share_frecuencia_natural": NTR[s] / sum(NTR.values())} for s in SITES])
pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:.4f}")
print(f"batches por epoca (estimados del indice) = {nb_tot:,.0f}\n")
print(d.to_string(index=False))
d.to_csv(Path(__file__).resolve().parent / "out" / "gradient_share.csv", index=False)
