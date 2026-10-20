"""Control negativo (tdew-077): TimesFM con la Tmin del horizonte real frente a barajada.

Evalua todos los directorios ``$WORK/preds_cribado_shuffle*`` que existan (``..._year`` es la
corrida original de 08_control_tmin_barajada.sh, semilla 0; ``..._<modo>_s<semilla>`` son las
de 11_control_tmin_barajada_semillas.sh) sobre las celdas y dias comunes con el run limpio de
Palacios (ll4) y con el cribado real. Cada directorio aporta una columna por variante.
"""
import glob
import os

import numpy as np
import pandas as pd

W = os.environ.get("TDEW_TIMESFM_WORK", "/home/cvelasquez/tdew_timesfm")
R = "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/tuning/backtest_clean/ll4/predictions.parquet"
VARIANTS = {"tmin_td_full": "td", "tmin_anom_full": "anom"}


def _label(directory: str) -> str:
    name = os.path.basename(directory).removeprefix("preds_cribado_shuffle_")
    return "year_s0" if name == "year" else name


ref = pd.read_parquet(R, columns=["ID", "FECHA", "TD_obs", "pred_clim", "pred_tuned"])
sources = [(f"real_{short}", f"{W}/preds_cribado/ll4__{key}.parquet") for key, short in VARIANTS.items()]
for directory in sorted(glob.glob(f"{W}/preds_cribado_shuffle*")):
    for key, short in VARIANTS.items():
        path = f"{directory}/ll4__{key}.parquet"
        if os.path.exists(path):
            sources.append((f"shuf_{short}_{_label(directory)}", path))

out = ref
for tag, path in sources:
    d = pd.read_parquet(path, columns=["ID", "FECHA", "pred"]).rename(columns={"pred": tag})
    out = out.merge(d, on=["ID", "FECHA"], how="inner")
print("celdas", out.ID.nunique(), "filas", len(out))
o = out.TD_obs.to_numpy("f8")


def rm(c: str) -> float:
    return float(np.sqrt(np.mean((out[c].to_numpy("f8") - o) ** 2)))


cl = rm("pred_clim")
for c in ["pred_clim", "pred_tuned", *(tag for tag, _ in sources)]:
    r = rm(c)
    print(f"{c:22s} rmse {r:.4f}  skill {1 - r / cl:+.3f}  bias {np.mean(out[c] - o):+.3f}")
