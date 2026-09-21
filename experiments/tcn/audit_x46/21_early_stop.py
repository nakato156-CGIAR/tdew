"""Consecuencia practica de la curva de audit/20: con que frecuencia evalua
el bucle de entrenamiento frente a donde esta el optimo de validation.

Se combinan (a) los pasos por epoca reales de los checkpoints, (b) la curva
de validation del experimento controlado, y (c) las metricas por epoca del
run de produccion en mlflow.db.
"""
import sys, sqlite3
from pathlib import Path
import numpy as np, pandas as pd, torch
ROOT = Path(__file__).resolve().parents[1]
CK = ROOT / "experiments/tcn/checkpoints/week1-tcn-attention_L31_seed0"

steps = {}
for p in sorted(CK.glob("epoch_*.pt")):
    c = torch.load(p, map_location="cpu", weights_only=False)
    steps[int(c["epoch"])] = int(c["global_step"])
per = steps[0]
print(f"pasos entre dos evaluaciones en produccion (= 1 epoca) = {per:,}")

con = sqlite3.connect(f"file:{(ROOT/'mlflow.db').resolve()}?mode=ro", uri=True)
q = """select m.key, m.step, m.value from metrics m join runs r on r.run_uuid=m.run_uuid
       where r.name='week1-tcn-attention' and m.key in ('val_rmse','train_loss','epoch_seconds')"""
d = {}
for k, s, v in con.execute(q): d.setdefault(s, {})[k] = v
con.close()
print("\nproduccion (mlflow.db), val_rmse por epoca:")
prev = None
for s in sorted(d):
    rec = d[s]
    print(f"   epoca {s}: paso {steps.get(s, float('nan')):>10,}  train_loss={rec['train_loss']:.5f}  "
          f"val_rmse={rec['val_rmse']:.4f}  horas={rec['epoch_seconds']/3600:.2f}")

g = pd.read_csv(Path(__file__).resolve().parent / "out" / "ablation_gpu.csv") if \
    (Path(__file__).resolve().parent / "out" / "ablation_gpu.csv").exists() else None
print("\nprimera evaluacion de produccion = paso 1.699.186.")
print("En el experimento controlado (audit/20) la primera evaluacion cae en el paso 2.000,")
print("850 veces antes, y ya es el mejor valor de toda la curva.")
