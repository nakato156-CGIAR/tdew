"""Inspecciona los checkpoints reales: epoch/global_step/best_val_skill,
estadisticas de pesos, y en particular la escala de gamma/beta de FiLM
(que multiplica la salida del TCN antes de la cabeza)."""
import sys, json
from pathlib import Path
import numpy as np, torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tdew_estimation.models import TCNAttentionConfig, TCNAttentionModel

CKDIR = ROOT / "experiments/tcn/checkpoints/week1-tcn-attention_L31_seed0"

for p in sorted(CKDIR.glob("*.pt")):
    ck = torch.load(p, map_location="cpu", weights_only=False)
    print(f"\n### {p.name}  size={p.stat().st_size}")
    print("   epoch          =", ck["epoch"])
    print("   global_step    =", ck["global_step"])
    print("   best_val_skill =", ck["best_val_skill"])
    print("   mlflow_run_id  =", ck.get("mlflow_run_id"))
    print("   config         =", json.dumps(ck["config"], sort_keys=True))

print("\n=== verificacion de carga estricta en el modelo del worktree ===")
model = TCNAttentionModel(TCNAttentionConfig())
last = torch.load(CKDIR / "last.pt", map_location="cpu", weights_only=False)
missing, unexpected = model.load_state_dict(last["model_state_dict"], strict=False)
print("   missing keys   =", missing)
print("   unexpected keys=", unexpected)
print("   n_parameters   =", model.num_parameters())

print("\n=== estadisticas de pesos por checkpoint ===")
for name in ["epoch_0000.pt", "epoch_0001.pt", "epoch_0002.pt", "epoch_0003.pt", "epoch_0004.pt"]:
    f = CKDIR / name
    if not f.exists():
        continue
    sd = torch.load(f, map_location="cpu", weights_only=False)["model_state_dict"]
    tot = sum(float((v.float() ** 2).sum()) for v in sd.values())
    print(f"\n-- {name}  ||theta||_2 = {tot**0.5:.6f}")
    for k in ["film.mlp.2.weight", "film.mlp.2.bias", "head.3.weight", "head.3.bias",
              "attention_pool.query", "input_proj.weight"]:
        if k in sd:
            v = sd[k].float()
            print(f"   {k:28s} shape={tuple(v.shape)} mean={v.mean():+.5f} std={v.std():.5f} absmax={v.abs().max():.5f}")

print("\n=== FiLM: escala efectiva de gamma y beta sobre estaticos reales-plausibles ===")
# gamma,beta se generan de film.mlp: las ultimas d_model columnas son beta.
sd = torch.load(CKDIR / "last.pt", map_location="cpu", weights_only=False)["model_state_dict"]
model.load_state_dict(sd)
model.eval()
d = model.config.d_model
W = sd["film.mlp.2.weight"].float(); b = sd["film.mlp.2.bias"].float()
print("   bias gamma  (primeras d_model):", f"mean={b[:d].mean():+.5f} std={b[:d].std():.5f} absmax={b[:d].abs().max():.5f}")
print("   bias beta   (ultimas d_model):", f"mean={b[d:].mean():+.5f} std={b[d:].std():.5f} absmax={b[d:].abs().max():.5f}")

print("\n=== head: peso asignado a pooled (FiLM) vs target_cond ===")
Wh = sd["head.0.weight"].float()  # [head_hidden, d_model + 4]
print("   head.0.weight shape", tuple(Wh.shape))
print("   ||W[:, :d_model]||_F =", float(Wh[:, :d].norm()))
print("   ||W[:, d_model:]||_F =", float(Wh[:, d:].norm()), " (target_cond: sin,cos,LST_DAY,LST_NIGHT)")
for j, nm in enumerate(["sin_doy(t+1)", "cos_doy(t+1)", "LST_DAY(t+1)", "LST_NIGHT(t+1)"]):
    print(f"      ||W[:, {nm}]|| = {float(Wh[:, d+j].norm()):.5f}")
print("   norma media por columna de pooled =", float(Wh[:, :d].norm(dim=0).mean()))
