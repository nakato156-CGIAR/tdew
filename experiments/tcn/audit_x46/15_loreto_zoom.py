"""Inspeccion directa de por que el modelo predice train-Loreto con RMSE
0.15 degC. Se miran series reales de una celda y la estructura del error."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (SITES, load_model, predict_norm, metrics, td_anom_stats,
                    DYNAMIC_COLS, sample_windows)

mean, std = td_anom_stats()
TD_IDX = DYNAMIC_COLS.index("TD_anom_norm")
model = load_model("last.pt")

for split in ["train", "validation"]:
    s = sample_windows(split, n_buckets=1, cells_per_site_per_bucket=4, seed=777, verbose=False)
    s["site"] = s["site"].astype(str)
    m = s["site"] == "iquitos_loreto"
    pn = predict_norm(model, s)
    lab, prd = s["label"][m], pn[m]
    tdt = s["dynamic"][m][:, -1, TD_IDX]
    ids, dts = s["id"][m], s["date_ordinal"][m]
    print(f"\n########## {split} / iquitos_loreto  n={m.sum()} celdas={len(np.unique(ids))} ##########")
    print(f"   std(label)={lab.std():.4f} std(pred)={prd.std():.4f} corr={np.corrcoef(lab,prd)[0,1]:.5f}")
    print(f"   RMSE norm={np.sqrt(np.mean((prd-lab)**2)):.4f}  ({np.sqrt(np.mean((prd-lab)**2))*std:.4f} degC)")
    print(f"   corr(label, TD(t))={np.corrcoef(lab,tdt)[0,1]:.5f}")
    # estructura temporal del label
    one = ids == np.unique(ids)[0]
    o = np.argsort(dts[one]); y = lab[one][o]; p = prd[one][o]; x = tdt[one][o]
    print(f"   celda {np.unique(ids)[0]}: primeros 12 valores")
    print(f"     label : " + " ".join(f"{v:+.3f}" for v in y[:12]))
    print(f"     pred  : " + " ".join(f"{v:+.3f}" for v in p[:12]))
    print(f"     TD(t) : " + " ".join(f"{v:+.3f}" for v in x[:12]))
    print(f"   autocorrelacion del label de esa celda: " +
          " ".join(f"lag{k}={np.corrcoef(y[:-k],y[k:])[0,1]:+.3f}" for k in [1,2,3,7,15,30,365]))
    d1 = np.diff(y)
    print(f"   std(label)={y.std():.4f}  std(diff diario del label)={d1.std():.4f}")
    # cuantos valores distintos toma el label en esa celda
    print(f"   valores distintos del label en la celda: {len(np.unique(np.round(y,6)))} de {len(y)}")
    # error por rango del label
    err = prd - lab
    q = np.quantile(np.abs(lab), [0.5, 0.9, 0.99])
    for lo, hi, nm in [(0, q[0], "|label|<p50"), (q[0], q[1], "p50-p90"), (q[1], q[2], "p90-p99"), (q[2], 99, ">p99")]:
        k = (np.abs(lab) >= lo) & (np.abs(lab) < hi)
        print(f"   {nm:12s} n={k.sum():>6d} rmse_norm={np.sqrt(np.mean(err[k]**2)):.4f}")
    # duplicados exactos de ventana
    h = np.ascontiguousarray(s["dynamic"][m]).view(np.uint8).reshape(int(m.sum()), -1)
    hs = pd.util.hash_array(np.frombuffer(h.tobytes(), dtype=np.int64))
    print(f"   ventanas duplicadas exactas (hash): {int(m.sum()) - len(np.unique(hs.reshape(int(m.sum()), -1), axis=0))}")
