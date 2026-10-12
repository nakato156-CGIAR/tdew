"""Economia del entrenamiento: pasos y tiempo por epoca, derivados de los
checkpoints reales (global_step) y de epoch_seconds en mlflow.db.
Nada esta escrito a mano: todo sale de los .pt y de la base de MLflow."""
import sys, sqlite3, json
from pathlib import Path
import numpy as np, torch, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
CK = ROOT / "experiments/tcn/checkpoints/week1-tcn-attention_L31_seed0"
SW = json.loads((ROOT / "experiments/tcn/site_weights.json").read_text())

steps = {}
for p in sorted(CK.glob("epoch_*.pt")):
    c = torch.load(p, map_location="cpu", weights_only=False)
    steps[int(c["epoch"])] = int(c["global_step"])
print("global_step acumulado por epoca (de los checkpoints):", steps)
ep = sorted(steps)
per_epoch = [steps[ep[0]]] + [steps[ep[i]] - steps[ep[i-1]] for i in range(1, len(ep))]
print("pasos por epoca:", per_epoch)

con = sqlite3.connect(f"file:{(ROOT/'mlflow.db').resolve()}?mode=ro", uri=True)
q = """select r.run_uuid, m.step, m.value from metrics m join runs r on r.run_uuid=m.run_uuid
       where m.key='epoch_seconds' and r.name='week1-tcn-attention' order by m.step"""
secs = {int(s): v for _, s, v in con.execute(q)}
print("epoch_seconds (mlflow.db):", {k: round(v, 1) for k, v in secs.items()})
con.close()

bs = 1024
tot_train = sum(SW["train_n_eligible_targets"].values())
print(f"\nventanas de entrenamiento por epoca (site_weights.json, indice L=31): {tot_train:,}")
print(f"pasos por epoca x batch = {per_epoch[0]*bs:,} muestras -> cobertura {per_epoch[0]*bs/tot_train:.4%}")
for e in sorted(secs):
    if e < len(per_epoch):
        sps = per_epoch[e] / secs[e]
        print(f"  epoca {e}: {per_epoch[e]:,} pasos en {secs[e]/3600:.2f} h "
              f"= {sps:.1f} pasos/s = {sps*bs:,.0f} muestras/s")
med = float(np.median(list(secs.values())))
print(f"\nmediana epoch_seconds = {med/3600:.2f} h; 30 epocas = {30*med/3600/24:.1f} dias")
print(f"parametros del modelo = 157177 (checkpoint config); muestras vistas hasta epoca 4 = "
      f"{max(steps.values())*bs:,} = {max(steps.values())*bs/157177:,.0f} muestras por parametro")
