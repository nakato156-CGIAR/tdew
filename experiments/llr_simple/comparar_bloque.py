"""TimesFM frente a LLR simple y climatologia en un bloque (tdew-03g). Sin `tuned`."""
import os
import sys
import numpy as np, pandas as pd

W = "/home/cvelasquez/tdew_timesfm"
split = sys.argv[1] if len(sys.argv) > 1 else "ll4b"
llr = pd.read_parquet(f"{W}/llr_simple/{split}__llr_simple.parquet")
df = llr
for tag, key in (("tfm_td", "tmin_td_full"), ("tfm_anom", "tmin_anom_full")):
    path = next((q for q in (f"{W}/preds_nacional_{split}/{split}__{key}.parquet", f"{W}/preds_nacional/{split}__{key}.parquet") if os.path.exists(q)), None)
    if path is None:
        continue
    p = pd.read_parquet(path, columns=["ID", "FECHA", "pred"])
    df = df.merge(p.rename(columns={"pred": tag}), on=["ID", "FECHA"], how="inner")
import os
_lp = f"{W}/llr_simple/{split}__llr_tmin_lags.parquet"
if os.path.exists(_lp):
    df = df.merge(pd.read_parquet(_lp, columns=["ID", "FECHA", "pred_llr_tmin_lags"]), on=["ID", "FECHA"], how="inner")
_tp = {"ll4b": f"{W}/tuning_ll4b/ll4b/predictions.parquet",
       "ll4": "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/tuning/backtest_clean/ll4/predictions.parquet"}.get(split)
if _tp and os.path.exists(_tp):
    df = df.merge(pd.read_parquet(_tp, columns=["ID", "FECHA", "pred_tuned"]), on=["ID", "FECHA"], how="inner")
df["y"] = df.FECHA.dt.year; df["m"] = df.FECHA.dt.month
o = df.TD_obs.to_numpy("f8")
print(split, "celdas", df.ID.nunique(), "filas", len(df))
cols = {"clim": "pred_clim", **({"tuned (Palacios)": "pred_tuned"} if "pred_tuned" in df else {}), "LLR simple": "pred_llr_simple", **({"LLR Tmin+rezagos": "pred_llr_tmin_lags"} if "pred_llr_tmin_lags" in df else {}), "TimesFM td": "tfm_td", "TimesFM anom": "tfm_anom"}
cols = {k: c for k, c in cols.items() if c in df}
for k, c in cols.items():
    e = df[c].to_numpy("f8") - o
    print(f"{k:13s} rmse {np.sqrt(np.mean(e**2)):.4f} bias {e.mean():+.3f} | " +
          " ".join(f"{y}:{np.sqrt(np.mean(e[df.y.to_numpy()==y]**2)):.3f}" for y in sorted(df.y.unique())))
rng = np.random.default_rng(0)
def boot(a, b, B=2000):
    se_a = (df[a] - df.TD_obs) ** 2; se_b = (df[b] - df.TD_obs) ** 2
    g = pd.DataFrame({"a": se_a, "b": se_b, "y": df.y, "m": df.m}).groupby(["y", "m"]).agg(n=("a", "size"), a=("a", "sum"), b=("b", "sum"))
    n, A, Bv = g.n.to_numpy(), g.a.to_numpy(), g.b.to_numpy(); r = []
    for _ in range(B):
        i = rng.integers(0, len(g), len(g)); N = n[i].sum()
        r.append(np.sqrt(A[i].sum() / N) - np.sqrt(Bv[i].sum() / N))
    pt = np.sqrt(se_a.mean()) - np.sqrt(se_b.mean())
    print(f"  {a} - {b}: {pt:+.4f}  IC mes-anio [{np.percentile(r,2.5):+.4f}, {np.percentile(r,97.5):+.4f}]  TimesFM/2do mejor en {(g.a>g.b).sum()}/{len(g)} meses")
print("brecha (positivo = el segundo gana), bloques mes-anio:")
if "tfm_td" in df: boot("pred_llr_simple", "tfm_td")
boot("pred_llr_simple", "tfm_anom")
if "pred_llr_tmin_lags" in df:
    boot("pred_llr_tmin_lags", "tfm_anom"); boot("pred_llr_simple", "pred_llr_tmin_lags")
boot("pred_clim", "pred_llr_simple")
if "pred_tuned" in df:
    boot("pred_tuned", "tfm_anom"); boot("pred_tuned", "pred_llr_simple")
    if "pred_llr_tmin_lags" in df: boot("pred_tuned", "pred_llr_tmin_lags")
