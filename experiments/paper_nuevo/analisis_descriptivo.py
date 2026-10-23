"""R2 (tdew-4w2): analisis descriptivo pedido por los revisores 1 (comentario 5) y 2 (3-5).

Todo es descriptivo (sin afirmaciones causales), por bloque (``ll4`` 2013-2016, ``ll4b`` 2009-2012)
y ambito (``panel`` 17.027 celdas, ``peru`` 8.272), sobre las filas comunes de
``experiments.amenazas.desglose.load_split``. Metodos: ``timesfm_anom``, ``tuned``,
``tuned_sin_td``, ``llr_rezagos_sel``, ``llr_simple_sel`` y ``clim``.

Salidas (``reports/paper_nuevo/resultados/``):

* ``r2_skill.csv``: skill de MSE frente a la climatologia (1 - MSE/MSE_clim), razon de varianzas
  var(anomalia predicha)/var(anomalia observada) y correlacion de anomalias. La anomalia es
  ``valor - clim`` (``clim`` = prediccion climatologica de la propia tabla); los momentos se
  calculan agrupados sobre todas las filas del ambito. Se anade el skill medio y mediano por celda.
* ``r2_extremos.csv``: RMSE y sesgo (pred - obs) en el 5 % de dias con mayor y menor anomalia
  observada de Td. Los umbrales (cuantiles 0,05 y 0,95 de ``TD_obs - clim``) se calculan POR
  CELDA sobre los dias del bloque completo (todos los anios del bloque, no solo el anio). Como la
  seleccion condiciona sobre el observado, el sesgo es negativo/positivo por construccion y solo
  sirve para comparar metodos entre si.
* ``r2_calibracion.csv``: solo TimesFM (``tuned`` y las LLR son deterministas; ``tuned`` no
  guarda cuantiles). Cobertura empirica del intervalo 80 % (q10-q90), anchura media, cuentas del
  histograma tipo PIT en las 10 clases que definen los 9 deciles (esperado 10 % por clase) y CRPS
  aproximado por cuadratura de pinball (``experiments.timesfm.probabilistic``).
* ``r2_estratos_altitud.csv``: RMSE por metodo y brecha TimesFM - metodo por banda de DEM
  (``kl_calido.DEM_EDGES``, DEM de ``Data/silver/static_covariates.parquet``) y por dentro/fuera
  del Peru dentro del panel. No hay capa de regiones naturales (costa/sierra/selva) en el
  repositorio y las letras de zona SENAMHI no son una regionalizacion natural, de modo que solo se
  estratifica por altitud.
* ``r2_sin_zona_dominante.csv``: peso de la zona con mas celdas del ambito (A (r) A' en ambos)
  en el agregado y brecha RMSE excluyendo esa zona.
* ``r2_enso.csv``: RMSE por metodo y brecha por clase ENSO mensual (El Nino: ONI >= 0,5; La Nina:
  ONI <= -0,5; neutral en otro caso). ONI de NOAA CPC (``oni.ascii.txt``), trimestre movil
  asignado a su mes central (DJF -> enero, ..., NDJ -> diciembre).

Brecha = RMSE(timesfm_anom) - RMSE(metodo); negativa favorece a TimesFM.

Uso: ``uv run python -m experiments.paper_nuevo.analisis_descriptivo [--splits ll4 ll4b]``
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd

from experiments.amenazas import desglose
from experiments.amenazas.desglose import OUT, RES, WORK, load_split
from experiments.timesfm import probabilistic

logger = logging.getLogger("paper_nuevo.analisis_descriptivo")

METHODS = ("timesfm_anom", "tuned", "tuned_sin_td", "llr_rezagos_sel", "llr_simple_sel", "clim")
REF = "timesfm_anom"
STATIC = Path("Data/silver/static_covariates.parquet")
ONI_PATH = WORK / "a4/isd_meta/oni.ascii.txt"
TAIL_Q = 0.05
ONI_THR = 0.5
DEM_EDGES = (0.0, 500.0, 1500.0, 2500.0, 3500.0)
DEM_LABELS = ("0-500", "500-1500", "1500-2500", "2500-3500", ">3500")
BEAD = "tdew-4w2"
FILES = {"skill": "r2_skill.csv", "extremos": "r2_extremos.csv", "calibracion": "r2_calibracion.csv",
         "altitud": "r2_estratos_altitud.csv", "sin_zona": "r2_sin_zona_dominante.csv",
         "enso": "r2_enso.csv"}
SEASONS = ("DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ")


# ------------------------------------------------------------------------------ helpers

def _codes(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    uniq, inv = np.unique(values, return_inverse=True)
    return inv.astype(np.int64), uniq


def dem_band(dem: np.ndarray) -> np.ndarray:
    """Banda de DEM (mismos bordes y etiquetas que ``kl_calido.dem_band``)."""
    idx = np.searchsorted(np.asarray(DEM_EDGES[1:]), dem, side="right")
    out = np.asarray(DEM_LABELS, dtype=object)[np.clip(idx, 0, len(DEM_LABELS) - 1)]
    out[~np.isfinite(dem)] = "sin_dem"
    return out


def anomalies(df: pd.DataFrame, methods: Sequence[str]) -> tuple[np.ndarray, dict[str, np.ndarray]]:
    """Anomalia observada y predicha (valor - clim)."""
    c = df["clim"].to_numpy("f8")
    return df["TD_obs"].to_numpy("f8") - c, {m: df[m].to_numpy("f8") - c for m in methods}


def skill_table(df: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    """Skill de MSE vs climatologia, razon de varianzas y correlacion de anomalias."""
    o = df["TD_obs"].to_numpy("f8")
    c = df["clim"].to_numpy("f8")
    ao = o - c
    mse_clim = np.mean((c - o) ** 2)
    codes, uniq = _codes(df["ID"].to_numpy())
    cnt = np.bincount(codes)
    mse_clim_cell = np.bincount(codes, (c - o) ** 2) / cnt
    rows = []
    for m in methods:
        p = df[m].to_numpy("f8")
        ap = p - c
        mse = np.mean((p - o) ** 2)
        mse_cell = np.bincount(codes, (p - o) ** 2) / cnt
        with np.errstate(divide="ignore", invalid="ignore"):
            sk_cell = 1.0 - mse_cell / mse_clim_cell
        sk_cell = sk_cell[np.isfinite(sk_cell)]
        va, vo = np.var(ap), np.var(ao)
        corr = np.nan if va == 0 or vo == 0 else float(np.corrcoef(ap, ao)[0, 1])
        rows.append({"metodo": m, "n": len(df), "celdas": len(uniq), "rmse": float(np.sqrt(mse)),
                     "mse": float(mse), "mse_clim": float(mse_clim),
                     "skill_mse": float(1.0 - mse / mse_clim),
                     "razon_varianza": float(va / vo) if vo > 0 else np.nan,
                     "razon_desv": float(np.sqrt(va / vo)) if vo > 0 else np.nan,
                     "corr_anomalia": corr,
                     "skill_celda_media": float(sk_cell.mean()) if sk_cell.size else np.nan,
                     "skill_celda_mediana": float(np.median(sk_cell)) if sk_cell.size else np.nan})
    return pd.DataFrame(rows)


def cell_thresholds(ids: np.ndarray, anom_obs: np.ndarray, q: float = TAIL_Q) -> tuple[np.ndarray, np.ndarray]:
    """Cuantiles q y 1-q de la anomalia observada, por celda, devueltos fila a fila."""
    ids, x = np.asarray(ids), np.asarray(anom_obs, "f8")
    return _fast_quantile(ids, x, q), _fast_quantile(ids, x, 1 - q)


def _fast_quantile(ids: np.ndarray, x: np.ndarray, q: float) -> np.ndarray:
    """Cuantil por grupo (interpolacion lineal, igual que pandas) sin transform en Python."""
    order = np.lexsort((x, ids))
    xs, ids_s = x[order], np.asarray(ids)[order]
    starts = np.r_[0, np.flatnonzero(ids_s[1:] != ids_s[:-1]) + 1]
    n = np.diff(np.r_[starts, len(xs)])
    pos = starts + q * (n - 1)
    lo = np.floor(pos).astype(np.int64)
    hi = np.minimum(lo + 1, starts + n - 1)
    val = xs[lo] + (pos - lo) * (xs[hi] - xs[lo])
    out = np.empty(len(x), "f8")
    out[order] = np.repeat(val, n)
    return out


def extremes_table(df: pd.DataFrame, methods: Sequence[str], lo: np.ndarray, hi: np.ndarray) -> pd.DataFrame:
    """RMSE y sesgo por cola (inferior/superior/resto) con umbrales por celda ``lo`` y ``hi``."""
    o = df["TD_obs"].to_numpy("f8")
    ao = o - df["clim"].to_numpy("f8")
    masks = {"inferior_5": ao <= lo, "superior_5": ao >= hi, "resto": (ao > lo) & (ao < hi)}
    rows = []
    for cls, mk in masks.items():
        for m in methods:
            e = df[m].to_numpy("f8")[mk] - o[mk]
            rows.append({"clase": cls, "metodo": m, "n": int(mk.sum()),
                         "rmse": float(np.sqrt(np.mean(e ** 2))) if mk.any() else np.nan,
                         "sesgo": float(e.mean()) if mk.any() else np.nan})
    return pd.DataFrame(rows)


def pit_counts(obs: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Cuentas de ``obs`` en las k+1 clases que definen k cuantiles por fila (``q`` ordenado)."""
    return np.bincount((obs[:, None] > q).sum(axis=1), minlength=q.shape[1] + 1)


def calibration_row(obs: np.ndarray, q: np.ndarray) -> dict:
    """Cobertura 80 %, anchura, histograma PIT y CRPS aproximado de deciles q10..q90."""
    ok = np.isfinite(obs) & np.isfinite(q).all(axis=1)
    obs, q = obs[ok], np.sort(q[ok], axis=1)
    cov = probabilistic.interval_coverage(obs, q[:, 0], q[:, -1])
    pit = pit_counts(obs, q)
    row = {"n": int(ok.sum()), "cobertura_80": cov["cobertura_80"], "anchura_80": cov["anchura_80"],
           "crps_aprox": probabilistic.crps_from_quantiles(obs, q),
           "pinball_medio": float(probabilistic.pinball(obs, q).mean()),
           "frac_bajo_q10": float(pit[0] / pit.sum()), "frac_sobre_q90": float(pit[-1] / pit.sum())}
    for i, c in enumerate(pit):
        row[f"pit_{i}"] = int(c)
    for i, c in enumerate(pit):
        row[f"pit_frac_{i}"] = float(c / pit.sum())
    return row


def classify_oni(anom: float, thr: float = ONI_THR) -> str:
    if not np.isfinite(anom):
        return "sin_dato"
    if anom >= thr:
        return "el_nino"
    if anom <= -thr:
        return "la_nina"
    return "neutral"


def oni_monthly(path: Path = ONI_PATH) -> pd.DataFrame:
    """ONI mensual (year, month, oni, clase): trimestre movil asignado a su mes central."""
    raw = pd.read_csv(path, sep=r"\s+")
    raw["month"] = raw["SEAS"].map({s: i + 1 for i, s in enumerate(SEASONS)})
    # NDJ de un anio YR esta centrado en diciembre de YR (la tabla de NOAA lo etiqueta con YR).
    out = raw.rename(columns={"YR": "year", "ANOM": "oni"})[["year", "month", "oni"]]
    out["clase"] = [classify_oni(v) for v in out["oni"]]
    return out


def grouped_rmse(df: pd.DataFrame, methods: Sequence[str], labels: np.ndarray, *, tipo: str,
                 extra_cols: Mapping[str, np.ndarray] | None = None) -> pd.DataFrame:
    """RMSE, sesgo y brecha TimesFM - metodo por etiqueta de estrato (filas con etiqueta NaN se omiten)."""
    keep = pd.notna(labels)
    codes, uniq = _codes(np.asarray(labels)[keep].astype(str))
    k = len(uniq)
    o = df["TD_obs"].to_numpy("f8")[keep]
    n = np.bincount(codes, minlength=k).astype("f8")
    ids = df["ID"].to_numpy()[keep]
    month_key = (df["year"].to_numpy(np.int64) * 100 + df["month"].to_numpy(np.int64))[keep]
    celdas = np.bincount(np.unique(codes * 100_000_000 + ids) // 100_000_000, minlength=k)
    meses = np.bincount(np.unique(codes * 1_000_000 + month_key) // 1_000_000, minlength=k)
    rmse, bias = {}, {}
    for m in methods:
        e = df[m].to_numpy("f8")[keep] - o
        rmse[m] = np.sqrt(np.bincount(codes, e ** 2, minlength=k) / n)
        bias[m] = np.bincount(codes, e, minlength=k) / n
    rows = []
    for j, lab in enumerate(uniq):
        for m in methods:
            rows.append({"estrato_tipo": tipo, "estrato": lab, "metodo": m, "n": int(n[j]),
                         "celdas": int(celdas[j]), "meses": int(meses[j]), "rmse": float(rmse[m][j]),
                         "sesgo": float(bias[m][j]),
                         "brecha_tfm_menos_metodo": float(rmse[REF][j] - rmse[m][j]) if m != REF and REF in rmse else np.nan})
    return pd.DataFrame(rows)


def dominant_zone_table(df: pd.DataFrame, methods: Sequence[str]) -> pd.DataFrame:
    """Peso de la zona con mas celdas y RMSE / brecha con y sin esa zona."""
    cells = df.drop_duplicates("ID")
    zid = cells["zone_id"].value_counts().idxmax()
    label = df.loc[df["zone_id"] == zid, "zone_label"].iloc[0]
    inz = (df["zone_id"] == zid).to_numpy()
    o = df["TD_obs"].to_numpy("f8")
    sse = {m: (df[m].to_numpy("f8") - o) ** 2 for m in methods}
    rm = lambda m, mk: float(np.sqrt(sse[m][mk].mean()))  # noqa: E731
    all_ = np.ones(len(df), bool)
    rows = []
    for m in methods:
        rows.append({
            "zona_dominante": label, "zone_id": int(zid), "celdas_zona": int(cells["zone_id"].eq(zid).sum()),
            "celdas_ambito": len(cells), "frac_celdas": float(cells["zone_id"].eq(zid).mean()),
            "frac_filas": float(inz.mean()), "metodo": m,
            "rmse_total": rm(m, all_), "rmse_zona": rm(m, inz), "rmse_sin_zona": rm(m, ~inz),
            "frac_sse_zona": float(sse[m][inz].sum() / sse[m].sum()),
            "brecha_total": rm(REF, all_) - rm(m, all_) if m != REF else np.nan,
            "brecha_zona": rm(REF, inz) - rm(m, inz) if m != REF else np.nan,
            "brecha_sin_zona": rm(REF, ~inz) - rm(m, ~inz) if m != REF else np.nan})
    return pd.DataFrame(rows)


# ------------------------------------------------------------------------------ carga

def add_dem(df: pd.DataFrame, static: Path = STATIC) -> pd.DataFrame:
    dem = pd.read_parquet(static, columns=["ID", "DEM"])
    dem = dem[dem.ID.isin(df.ID.unique())].drop_duplicates("ID")
    df = df.merge(dem, on="ID", how="left")
    df["dem_band"] = dem_band(df["DEM"].to_numpy("f8"))
    return df


def load_quantiles(split: str, df: pd.DataFrame) -> tuple[np.ndarray, str]:
    """Deciles de TimesFM alineados con las filas de ``df`` (mismo orden ID, FECHA)."""
    tfm_dir = WORK / ("preds_nacional" if split == "ll4" else f"preds_nacional_{split}")
    path = tfm_dir / f"{split}__tmin_anom_full.parquet"
    q = pd.read_parquet(path, columns=["ID", "FECHA", *probabilistic.COLUMNS])
    key = df[["ID", "FECHA"]]
    q = key.merge(q, on=["ID", "FECHA"], how="left")
    return q[list(probabilistic.COLUMNS)].to_numpy("f8"), str(path)


# ------------------------------------------------------------------------------ corrida

def run(splits: Sequence[str], out: Path = OUT) -> dict[str, pd.DataFrame]:
    out.mkdir(parents=True, exist_ok=True)
    oni = oni_monthly()
    tabs: dict[str, list[pd.DataFrame]] = {k: [] for k in FILES}
    inputs: dict[str, dict[str, str]] = {}
    for split in splits:
        df, _, used = load_split(split)
        methods = [m for m in METHODS if m in df]
        keep_cols = ["ID", "FECHA", "TD_obs", "zone_id", "zone_label", "peru", "year", "month", *methods]
        df = add_dem(df[keep_cols]).copy()
        qarr, qpath = load_quantiles(split, df)
        used = {m: used[m] for m in methods} | {"timesfm_cuantiles": qpath, "dem": str(STATIC), "oni": str(ONI_PATH)}
        inputs[split] = used
        ao = df["TD_obs"].to_numpy("f8") - df["clim"].to_numpy("f8")
        lo, hi = cell_thresholds(df["ID"].to_numpy(), ao)
        df["_lo"], df["_hi"] = lo, hi
        df = df.merge(oni[["year", "month", "oni", "clase"]], on=["year", "month"], how="left")
        logger.info("%s: %d filas, metodos %s", split, len(df), methods)
        for ambito in ("panel", "peru"):
            mk = np.ones(len(df), bool) if ambito == "panel" else df["peru"].to_numpy()
            sub = df[mk].reset_index(drop=True)
            q = qarr[mk]
            tag = {"split": split, "ambito": ambito}
            tabs["skill"].append(skill_table(sub, methods).assign(**tag))
            tabs["extremos"].append(extremes_table(sub, methods, sub["_lo"].to_numpy(), sub["_hi"].to_numpy()).assign(**tag))
            obs = sub["TD_obs"].to_numpy("f8")
            for per in ["total"] + [str(y) for y in sorted(sub.year.unique())]:
                pm = np.ones(len(sub), bool) if per == "total" else (sub["year"] == int(per)).to_numpy()
                tabs["calibracion"].append(pd.DataFrame([{"periodo": per, **calibration_row(obs[pm], q[pm])}]).assign(**tag))
            alt = grouped_rmse(sub, methods, sub["dem_band"].to_numpy(), tipo="altitud")
            tabs["altitud"].append(alt.assign(**tag))
            if ambito == "panel":
                pf = np.where(sub["peru"].to_numpy(), "peru", "fuera_peru")
                tabs["altitud"].append(grouped_rmse(sub, methods, pf, tipo="peru_fuera").assign(**tag))
            tabs["sin_zona"].append(dominant_zone_table(sub, methods).assign(**tag))
            tabs["enso"].append(grouped_rmse(sub, methods, sub["clase"].to_numpy(), tipo="enso").assign(**tag))
        del df
    result = {}
    front = ["split", "ambito"]
    for k, name in FILES.items():
        t = pd.concat(tabs[k], ignore_index=True)
        t = t[front + [c for c in t.columns if c not in front]]
        t.to_csv(out / name, index=False, float_format="%.5f")
        result[k] = t
    write_provenance([str(out / n) for n in FILES.values()], inputs, splits)
    return result


def write_provenance(output_files: list[str], inputs: dict, splits: Sequence[str]) -> None:
    from tdew_estimation import provenance as prov

    train_end = desglose.TRAIN_END
    notes = ("R2 descriptivo (revisores 1.5 y 2.3-2.5): skill vs clim, razon de varianzas, correlacion de "
             f"anomalias, extremos (umbrales por celda {TAIL_Q:g}/{1 - TAIL_Q:g} sobre TD_obs - clim del bloque), "
             "calibracion de deciles de TimesFM, estratos de altitud (DEM), peso de la zona dominante y "
             f"clases ENSO (ONI >= {ONI_THR} El Nino, <= -{ONI_THR} La Nina; trimestre movil en su mes central). "
             f"Metodos {list(METHODS)}; brecha = RMSE(timesfm_anom) - RMSE(metodo). Filas comunes de "
             f"desglose.load_split; mascara Peru = peru_mask. Entradas: {inputs}")
    record = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id=BEAD, manifest_ref="docs/protocol/timesfm_manifest.yaml",
        model_family="comparison", model_id="multi", variant_label="r2_descriptivo",
        trained=True, training_period=("1981-01-01", f"{max(train_end[s] for s in splits)}-12-31"),
        validation_period=None,
        test_period=(f"{min(train_end[s] for s in splits) + 1}-01-01",
                     f"{max(train_end[s] for s in splits) + 4}-12-31"),
        split_id=",".join(splits), autoregressive=True, target_type="td_raw",
        climatology_used=True, climatology_role="baseline_and_anomaly_reference",
        inputs=tuple(sorted({m for d in inputs.values() for m in d})),
        panel_id="nacional_17027", panel_cell_count=17027, panel_file=str(desglose.PANEL),
        output_files=tuple(output_files), seeds=(), notes=notes,
    )
    prov.record_metric_provenance(record)


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--splits", nargs="+", default=["ll4", "ll4b"])
    ap.add_argument("--out", type=Path, default=OUT)
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")
    run(a.splits, a.out)


if __name__ == "__main__":
    main()
