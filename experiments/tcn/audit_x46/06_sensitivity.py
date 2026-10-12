"""Que aprendio el modelo entrenado: sensibilidad de la prediccion a cada
bloque de entrada y a cada canal dinamico, estadisticas internas de FiLM y
de la atencion, medidas sobre la misma submuestra de validation.

Subconjunto: las primeras N_SUB ventanas de la submuestra cacheada tras una
permutacion con semilla fija (para no gastar CPU en 559k ventanas por cada
ablacion).
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd, torch
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, STATIC_COLS, TARGET_COND_COLS)

OUT = Path(__file__).resolve().parent / "out"
val = dict(np.load(OUT / "sample_validation.npz"))
val["site"] = val["site"].astype(str)
mean, std = td_anom_stats()
rng = np.random.default_rng(1234)
N_SUB = 60000
idx = rng.permutation(len(val["label"]))[:N_SUB]
sub = {k: v[idx] for k, v in val.items()}
obs = sub["label"] * std + mean + sub["td_clim"]
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
print(f"subconjunto de {N_SUB} ventanas (permutacion seed=1234 de la submuestra de validation)")

for ckname in ["best.pt", "last.pt"]:
    model = load_model(ckname)
    base = predict_norm(model, sub)
    base_phys = base * std + mean + sub["td_clim"]
    m0 = metrics(base_phys, obs)
    print(f"\n########## {ckname} ##########")
    print(f"prediccion base: rmse={m0['rmse']:.4f} mae={m0['mae']:.4f} bias={m0['bias']:+.4f} r={m0['r']:.5f}")
    print(f"pred_norm: mean={base.mean():+.4f} std={base.std():.4f} min={base.min():+.3f} max={base.max():+.3f}")
    print(f"label    : mean={sub['label'].mean():+.4f} std={sub['label'].std():.4f}")
    print(f"corr(pred_norm, label)             = {np.corrcoef(base, sub['label'])[0,1]:.5f}")
    print(f"corr(pred_norm, TD_anom_norm(t))   = {np.corrcoef(base, sub['dynamic'][:,-1,TD_IDX])[0,1]:.5f}")
    print(f"pendiente OLS label~pred (shrink)  = "
          f"{np.polyfit(base, sub['label'], 1)[0]:.4f}")

    rows = []
    def ab(name, **kw):
        p = predict_norm(model, sub, **kw)
        ph = p * std + mean + sub["td_clim"]
        m = metrics(ph, obs)
        rows.append({"ablacion": name, "rmse": m["rmse"], "d_rmse": m["rmse"] - m0["rmse"],
                     "corr_con_pred_base": float(np.corrcoef(p, base)[0, 1]),
                     "std_pred": float(p.std())})

    z = np.zeros_like
    ab("ninguna (base)")
    ab("dynamic := 0 (toda la ventana)", dynamic=z(sub["dynamic"]))
    ab("dynamic barajado entre muestras", dynamic=sub["dynamic"][rng.permutation(N_SUB)])
    for j, c in enumerate(DYNAMIC_COLS):
        d = sub["dynamic"].copy(); d[:, :, j] = 0.0
        ab(f"dynamic[:,:,{j}] {c} := 0", dynamic=d)
    for keep in [1, 3, 7, 14]:
        d = sub["dynamic"].copy(); d[:, :-keep, :] = 0.0
        ab(f"solo ultimos {keep} dias de la ventana", dynamic=d)
    d = sub["dynamic"].copy(); d[:, -1, :] = 0.0
    ab("ultimo dia (t) := 0", dynamic=d)
    ab("static := 0", static=z(sub["static"]))
    ab("region := 0 (Costa para todos)", region=z(sub["region"]))
    ab("target_cond := 0", target_cond=z(sub["target_cond"]))
    for j, c in enumerate(TARGET_COND_COLS):
        tc = sub["target_cond"].copy(); tc[:, j] = 0.0
        ab(f"target_cond[:,{j}] {c} := 0", target_cond=tc)
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 200, "display.float_format", lambda v: f"{v:.4f}")
    print(df.to_string(index=False))
    df.to_csv(OUT / f"sensitivity_{ckname}.csv", index=False)

    # --- internos: FiLM y atencion ---
    with torch.no_grad():
        n = 8192
        dyn = torch.from_numpy(sub["dynamic"][:n]); sta = torch.from_numpy(sub["static"][:n])
        reg = torch.from_numpy(sub["region"][:n]); tc = torch.from_numpy(sub["target_cond"][:n])
        h = model.input_proj(dyn); h = model.tcn(h)
        pooled = model.attention_pool(h)
        gamma, beta = model.film(sta, reg)
        mod = gamma * pooled + beta
        print(f"\n-- internos ({n} ventanas)")
        print(f"   ||pooled|| medio        = {pooled.norm(dim=1).mean():.4f}")
        print(f"   gamma: mean={gamma.mean():+.4f} std={gamma.std():.4f} |gamma| medio={gamma.abs().mean():.4f}")
        print(f"   beta : mean={beta.mean():+.4f} std={beta.std():.4f} |beta| medio={beta.abs().mean():.4f}")
        print(f"   ||gamma*pooled|| medio  = {(gamma*pooled).norm(dim=1).mean():.4f}")
        print(f"   ||beta|| medio          = {beta.norm(dim=1).mean():.4f}")
        print(f"   ||gamma*pooled||/||beta|| = {float((gamma*pooled).norm(dim=1).mean()/beta.norm(dim=1).mean()):.4f}")
        # cuanta varianza de la entrada de la cabeza viene de la ventana vs del sitio
        var_win = (gamma * pooled).var(dim=0).sum()
        var_beta = beta.var(dim=0).sum()
        print(f"   var total de gamma*pooled entre muestras = {float(var_win):.4f}")
        print(f"   var total de beta        entre muestras = {float(var_beta):.4f}")
        aw = model.attention_pool.last_attn_weights  # [n, T+1]
        aw = aw.numpy()
        print(f"   atencion (query->[query, t-30..t]): shape={aw.shape}")
        print(f"     peso al propio query  = {aw[:,0].mean():.5f}")
        prof = aw[:, 1:].mean(0)
        print(f"     perfil medio por lag (t-30 .. t):")
        print("      " + " ".join(f"{v:.4f}" for v in prof))
        print(f"     uniforme seria {1/aw.shape[1]:.4f}; max={prof.max():.4f} en lag t-{30-int(prof.argmax())}")
