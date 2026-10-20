"""Chequeo de la Tmin regridada 2017-2020 frente a la Tmin 2013-2016 en las mismas celdas.

Celdas: panel nacional (``reports/timesfm_benchmark/panels/nacional_17027.csv``).
Fuentes (solo lectura): ``$RES/future_tmin_by_bucket`` (2017-2020, PISCOt v1.2 regridado
a la grilla de 2,8 M) y ``$RES/bucketed_training_data`` (TMIN 2013-2016, misma version).
Los dos periodos no se solapan, asi que no hay correlacion dia a dia; se reportan
distribucion por mes, medias por celda y mes (correlacion entre periodos del ciclo
anual por celda) y la discontinuidad dic-2016 / ene-2017.

Uso::

    uv run python -m experiments.a4_externo.tmin_check
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.timesfm import paths

from . import grid

logger = logging.getLogger("a4.tmin_check")
PANEL = Path("reports/timesfm_benchmark/panels/nacional_17027.csv")
OUT = Path("reports/paper_nuevo/resultados")
QUANTILES = (0.05, 0.25, 0.5, 0.75, 0.95)


def load(ids: np.ndarray) -> pd.DataFrame:
    past = grid.read_cells(paths.RES / "bucketed_training_data",
                           [f"train_{y}.parquet" for y in range(2013, 2017)], ids, ["ID", "FECHA", "TMIN"])
    past["periodo"] = "2013-2016"
    fut = grid.read_cells(paths.RES / "future_tmin_by_bucket",
                          [f"future_tmin_{y}.parquet" for y in range(2017, 2021)], ids, ["ID", "FECHA", "TMIN"])
    fut["periodo"] = "2017-2020"
    frame = pd.concat([past, fut], ignore_index=True).dropna(subset=["TMIN"])
    frame["FECHA"] = pd.to_datetime(frame["FECHA"])
    frame["mes"] = frame["FECHA"].dt.month
    frame["anio"] = frame["FECHA"].dt.year
    return frame


def summarize(frame: pd.DataFrame) -> dict[str, pd.DataFrame]:
    def stats(g):
        q = g["TMIN"].quantile(list(QUANTILES))
        row = {"n": len(g), "n_celdas": g["ID"].nunique(), "media": g["TMIN"].mean(), "sd": g["TMIN"].std()}
        row.update({f"p{int(k * 100):02d}": v for k, v in q.items()})
        return pd.Series(row)

    by_month = frame.groupby(["mes", "periodo"]).apply(stats).reset_index()
    overall = frame.groupby("periodo").apply(stats).reset_index()
    by_year = frame.groupby("anio").apply(stats).reset_index()

    cell_month = frame.groupby(["ID", "mes", "periodo"])["TMIN"].mean().unstack("periodo").dropna()
    d = cell_month["2017-2020"] - cell_month["2013-2016"]
    # anomalia de cada celda: quita la media de la celda en el periodo, deja solo el ciclo anual
    anom = cell_month - cell_month.groupby(level="ID").transform("mean")
    corr = pd.DataFrame([{
        "n_celdas": cell_month.index.get_level_values("ID").nunique(),
        "r_media_celda_mes": np.corrcoef(cell_month["2013-2016"], cell_month["2017-2020"])[0, 1],
        "r_ciclo_anual_celda": np.corrcoef(anom["2013-2016"], anom["2017-2020"])[0, 1],
        "dif_media": d.mean(), "dif_sd": d.std(),
        "dif_p05": d.quantile(0.05), "dif_p50": d.median(), "dif_p95": d.quantile(0.95),
        "frac_celdas_mes_absdif_gt_1C": float((d.abs() > 1).mean()),
    }])
    # salto dic(y-1) -> ene(y) por celda: el de 2016->2017 cruza el cambio de archivo
    monthly = frame.groupby(["ID", "anio", "mes"])["TMIN"].mean()
    rows = []
    for year in range(2014, 2021):
        jan = monthly.xs((year, 1), level=("anio", "mes"))
        dec = monthly.xs((year - 1, 12), level=("anio", "mes"))
        jump = (jan - dec).dropna()
        rows.append({"salto": f"ene{year} - dic{year - 1}", "cruza_archivo": year == 2017,
                     "media": jump.mean(), "sd": jump.std(), "p05": jump.quantile(0.05),
                     "p95": jump.quantile(0.95), "n_celdas": len(jump)})
    seam = pd.DataFrame(rows)
    return {"a4_tmin_por_mes": by_month, "a4_tmin_global": overall, "a4_tmin_por_anio": by_year,
            "a4_tmin_celda_mes": corr, "a4_tmin_costura": seam}


def roughness(n_buckets: int = 64) -> pd.DataFrame:
    """Diferencia de Tmin media entre celdas vecinas de una misma fila, por periodo y año.

    Los buckets 0..n-1 contienen tramos de n IDs consecutivos (``ID % 8192``), es decir
    tramos de fila de la grilla. Si el regrid de 2017-2020 fuera distinto al de 1981-2016
    (p. ej. vecino mas cercano frente a bilineal), la textura espacial cambiaria.
    """
    def read(root, names):
        parts = []
        for b in range(n_buckets):
            for name in names:
                path = grid.bucket_dir(root, b) / name
                t = pd.read_parquet(path, columns=["ID", "FECHA", "TMIN"])
                t["anio"] = pd.to_datetime(t["FECHA"]).dt.year
                parts.append(t.groupby(["ID", "anio"])["TMIN"].mean().reset_index())
        return pd.concat(parts, ignore_index=True)

    past = read(paths.RES / "bucketed_training_data", [f"train_{y}.parquet" for y in range(2013, 2017)])
    fut = read(paths.RES / "future_tmin_by_bucket", [f"future_tmin_{y}.parquet" for y in range(2017, 2021)])
    frame = pd.concat([past, fut], ignore_index=True).dropna()
    rows = []
    for year, g in frame.groupby("anio"):
        s = g.set_index("ID")["TMIN"]
        nxt = s.reindex(s.index + 1)
        same_row = (s.index % grid.NCOL) != grid.NCOL - 1
        d = (nxt.to_numpy() - s.to_numpy())[same_row]
        d = d[np.isfinite(d)]
        rows.append({"anio": year, "n_pares": len(d), "sd_dif_vecinos": float(np.std(d)),
                     "mad_dif_vecinos": float(np.median(np.abs(d))), "frac_dif_cero": float(np.mean(d == 0))})
    return pd.DataFrame(rows)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--panel", type=Path, default=PANEL)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    ids = pd.read_csv(args.panel)["ID"].to_numpy()
    frame = load(ids)
    logger.info("filas %d, celdas %d", len(frame), frame["ID"].nunique())
    args.out.mkdir(parents=True, exist_ok=True)
    for name, table in summarize(frame).items():
        table.to_csv(args.out / f"{name}.csv", index=False, float_format="%.4f")
        logger.info("%s\n%s", name, table.to_string())
    rough = roughness()
    rough.to_csv(args.out / "a4_tmin_rugosidad.csv", index=False, float_format="%.4f")
    logger.info("rugosidad\n%s", rough.to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
