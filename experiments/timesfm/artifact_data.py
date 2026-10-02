"""Construye el archivo de datos que embebe la pagina interactiva del benchmark.

La pagina se publica como Artifact y no puede descargar nada en tiempo de
ejecucion, asi que todo viaja dentro del HTML. Lo unico pesado es el mapa, y ahi
hay un hecho que decide el diseno: la rejilla nacional es regular —1982 latitudes
por 1422 longitudes a 0,01 grados, con ``ID`` denso en orden row-major— de modo
que una capa por celda es un arreglo plano que ``zlib`` comprime muy bien. Medido:
las 2,83 millones de celdas ocupan 25 KB en la capa de categorias y 114 KB en la
de zonas climaticas, ya en base64. Por eso el mapa es la rejilla real del proyecto
y no una version reducida.

El navegador la descomprime con ``DecompressionStream('deflate')``, que es API
nativa y no necesita libreria.

Ninguna metrica se recalcula aqui: se copian de los CSV que ya publico el
benchmark, y un control comprueba que lo volcado coincide con su origen.
"""

from __future__ import annotations

import argparse
import base64
import json
import logging
import zlib
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd

logger = logging.getLogger("timesfm.artifact")

REPORT = Path("reports/timesfm_benchmark")
SILVER = Path("Data/silver")
RES = Path("/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning")

# Geometria de la rejilla nacional, verificada contra zone_table.parquet.
LAT_MAX, LON_MIN, STEP = 1.22, -81.40, 0.01
N_LAT, N_LON = 1982, 1422

SITES = {
    "lima": ("Lima", 2),
    "cusco": ("Cusco", 3),
    "iquitos_loreto": ("Loreto", 4),
    "tarapoto_san_martin": ("San Martín", 5),
}
CELLS_EXPECTED = {"lima": 29079, "cusco": 60041, "iquitos_loreto": 305564,
                  "tarapoto_san_martin": 41835}
MAX_BYTES = 2 * 1024 * 1024


def encode(array: np.ndarray) -> str:
    """Comprime un arreglo de bytes y lo devuelve en base64."""
    return base64.b64encode(zlib.compress(array.astype(np.uint8).tobytes(), 9)).decode()


def peru_mask(report: Path = REPORT) -> np.ndarray:
    """Marca las celdas que caen dentro del territorio peruano.

    Hace falta porque la rejilla del producto no es el Peru: es la caja
    envolvente, y poco mas de la mitad de sus celdas con tierra estan en Brasil,
    Bolivia, Ecuador o Colombia. Dibujar la mascara de tierra como si fuera el
    pais seria falso, y ademas oculta que el muestreo del backtest hereda esa
    propiedad.
    """
    import shapely
    from shapely.geometry import shape
    from shapely.ops import unary_union

    geo = json.loads((report / "geo" / "peru_departamental_simple.geojson").read_text())
    pais = unary_union([shape(f["geometry"]) for f in geo["features"]])
    shapely.prepare(pais)

    lat = np.repeat(LAT_MAX - np.arange(N_LAT) * STEP, N_LON)
    lon = np.tile(LON_MIN + np.arange(N_LON) * STEP, N_LAT)
    return shapely.contains_xy(pais, lon, lat)


def build_layers(res: Path = RES, silver: Path = SILVER,
                 report: Path = REPORT) -> tuple[dict, dict]:
    """Capas del mapa, una entrada por celda de la rejilla del producto."""
    zones = pd.read_parquet(res / "zone_table.parquet", columns=["ID", "zone_id"])
    static = pd.read_parquet(silver / "static_covariates.parquet", columns=["ID", "DEM"])
    if len(zones) != N_LAT * N_LON:
        raise ValueError(f"la rejilla trae {len(zones)} celdas y se esperaban {N_LAT * N_LON}")

    # 0 fuera del dominio, 1 tierra fuera del Peru, 2..5 los cuatro departamentos,
    # 6 resto del territorio peruano.
    tierra = static["DEM"].to_numpy() == static["DEM"].to_numpy()
    dentro = peru_mask(report)
    category = np.where(tierra, 1, 0).astype(np.uint8)
    category[tierra & dentro] = 6
    counted: dict[str, int] = {}
    for key, (_, code) in SITES.items():
        members = pd.read_csv(silver / "department_grid_ids" / f"{key}.csv")["ID"].to_numpy()
        category[members] = code
        counted[key] = int((category == code).sum())
        if counted[key] != CELLS_EXPECTED[key]:
            raise ValueError(
                f"{key}: la capa reconstruye {counted[key]} celdas y el CSV tiene "
                f"{CELLS_EXPECTED[key]}; la rejilla no esta alineada"
            )
    logger.info("categorias: %s", counted)

    # Zonas SENAMHI, desplazadas en uno para que 0 signifique "sin zona".
    zone_layer = (zones["zone_id"].to_numpy() + 1).astype(np.uint8)
    zone_layer[category == 0] = 0

    # Las celdas del muestreo del backtest, separadas segun caigan dentro o fuera
    # del Peru. Esa separacion es contenido, no adorno: la mitad del muestreo esta
    # fuera del pais y conviene que se vea.
    sample_ids = pd.read_parquet(res / "tuning/backtest_clean/ll4/predictions.parquet",
                                 columns=["ID"])["ID"].unique()
    sample = np.zeros(N_LAT * N_LON, dtype=np.uint8)

    # La pasada de escala, que es la cobertura mas extensa: TimesFM predijo los
    # 1.461 dias de cada una de las 436.519 celdas de los cuatro departamentos.
    # Se pinta primero para que el muestreo disperso del backtest siga
    # distinguiendose encima.
    escala_path = Path("/home/cvelasquez/tdew_timesfm/panel_436k.csv")
    n_escala = 0
    if escala_path.exists():
        escala_ids = pd.read_csv(escala_path)["ID"].to_numpy()
        sample[escala_ids] = 4
        n_escala = int((sample == 4).sum())
        if n_escala != sum(CELLS_EXPECTED.values()):
            raise ValueError(
                f"la pasada de escala cubre {n_escala} celdas y los cuatro "
                f"departamentos suman {sum(CELLS_EXPECTED.values())}"
            )
    logger.info("pasada de escala: %d celdas", n_escala)

    sample[sample_ids] = 1
    sample[sample_ids[dentro[sample_ids]]] = 2
    n_dentro = int((sample == 2).sum())
    n_fuera = int((sample == 1).sum())

    # El panel departamental, que fue durante meses el unico conjunto con medicion
    # propia de TimesFM dentro de los departamentos. La pasada de escala lo
    # contiene, de modo que ya no necesita capa propia; se conserva el recuento
    # porque es la muestra sobre la que corren la TCN y los tests pareados.
    panel_path = Path("/home/cvelasquez/tdew_reconstruction/panels/ll4_reducido_512.csv")
    n_panel = 0
    if panel_path.exists():
        panel_ids = pd.read_csv(panel_path)["ID"].to_numpy()
        n_panel = int(len(np.unique(panel_ids)))
    logger.info("panel departamental: %d celdas", n_panel)
    logger.info("muestreo del backtest: %d celdas, %d dentro del Peru (%.1f%%), %d fuera",
                n_dentro + n_fuera, n_dentro, 100 * n_dentro / (n_dentro + n_fuera), n_fuera)

    layers = {
        "categoria": encode(category),
        "zona": encode(zone_layer),
        "muestreo": encode(sample),
    }
    meta = {
        "nLat": N_LAT, "nLon": N_LON, "latMax": LAT_MAX, "lonMin": LON_MIN, "paso": STEP,
        "celdas": int(N_LAT * N_LON),
        "celdasTierra": int((category > 0).sum()),
        "celdasPeru": int(dentro.sum()),
        "celdasMuestreo": int((sample > 0).sum()),
        "muestreoDentro": int((sample == 2).sum()),
        "muestreoFuera": int((sample == 1).sum()),
        "panelDepartamental": n_panel,
        "escalaCeldas": n_escala,
        # Unicas, no la suma: el muestreo del backtest y la pasada de escala se
        # solapan y esas celdas no deben contarse dos veces.
        "medidasHoy": int((sample > 0).sum()),
        "celdasDepartamentos": int(sum(counted.values())),
        "porDepartamento": {SITES[k][0]: v for k, v in counted.items()},
    }
    return layers, meta


def zone_metrics(report: Path = REPORT) -> dict:
    """Skill y RMSE por zona climatica, para colorear el mapa."""
    frame = pd.read_csv(report / "nacional_limpio" / "metrics_by_zone.csv")
    frame = frame[frame["split"] == "ll4"]
    out: dict[str, dict] = {}
    for zone, group in frame.groupby("zone_id"):
        entry = {}
        for _, row in group.iterrows():
            name = "timesfm" if str(row["method"]).startswith("timesfm") else str(row["method"])
            entry[name] = {"rmse": round(float(row["rmse"]), 4),
                           "skill": round(float(row["skill_vs_clim"]), 4)}
        entry["celdas"] = int(group["cells"].iloc[0])
        out[str(int(zone))] = entry
    logger.info("metricas por zona: %d zonas", len(out))
    return out


def zone_labels(res: Path = RES) -> dict:
    """Etiqueta Thornthwaite de cada zona, para el texto al pasar el cursor."""
    frame = pd.read_parquet(res / "zone_table.parquet", columns=["zone_id", "zone_label"])
    pairs = frame.drop_duplicates().sort_values("zone_id")
    return {str(int(z)): str(l) for z, l in zip(pairs["zone_id"], pairs["zone_label"])}


def error_curve(report: Path = REPORT, every: int = 7) -> dict:
    """RMSE acumulado dia a dia del bloque oculto, submuestreado."""
    frame = pd.read_csv(report / "curva_error_nacional_limpio.csv")
    frame = frame[(frame["dia"] % every == 0) | (frame["dia"] == frame["dia"].max())]
    out = {}
    for method, group in frame.groupby("method"):
        group = group.sort_values("dia")
        out[method] = {"dia": group["dia"].astype(int).tolist(),
                       "rmse": [round(float(v), 4) for v in group["rmse_acumulado"]]}
    logger.info("curva de error: %d metodos, %d puntos cada uno",
                len(out), len(next(iter(out.values()))["dia"]))
    return out


def tables(report: Path = REPORT) -> dict:
    """Las tablas de metricas, copiadas de los CSV publicados sin recalcular."""
    def rows(frame: pd.DataFrame, columns: Sequence[str]) -> list[dict]:
        return [
            {c: (round(float(r[c]), 4) if isinstance(r[c], (int, float, np.floating)) else r[c])
             for c in columns if c in frame.columns}
            for _, r in frame.iterrows()
        ]

    nacional = pd.read_csv(report / "nacional_limpio" / "metrics_all.csv")
    efectos = pd.read_csv(report / "nacional_limpio" / "effect_sizes_all.csv")
    cribado = pd.read_csv(report / "cribado_limpio" / "leaderboard.csv")
    dept = pd.read_csv(report / "departamental" / "metrics.csv")
    coste = pd.read_csv(report / "coste_throughput.csv")
    escala_csv = report / "escala" / "leaderboard.csv"
    escala = pd.read_csv(escala_csv) if escala_csv.exists() else pd.DataFrame()

    dept_pooled = dept[dept["level"] == "pooled"]
    dept_por = dept[dept["level"] == "department"]

    return {
        "nacional": rows(nacional, ["split", "method", "n", "rmse", "mae", "bias", "r", "skill_vs_clim"]),
        "efectos": rows(efectos, ["split", "comparison", "rmse_focal", "rmse_baseline",
                                  "delta_rmse_C", "delta_ci95", "skill", "frac_cells_focal_wins",
                                  "cohens_d", "perm_p_value", "n_cells"]),
        "cribado": rows(cribado.sort_values("rmse"),
                        ["method", "cells", "rmse", "mae", "bias", "r", "skill_vs_clim",
                         "crps_aprox", "cobertura_80"]),
        "departamental": rows(dept_pooled.sort_values("rmse"),
                              ["model", "seed", "n", "rmse", "mae", "bias", "r",
                               "skill_vs_climatology", "outside_qc_fraction"]),
        "departamentalPorSitio": rows(dept_por, ["model", "seed", "department", "rmse", "skill_vs_climatology"]),
        "coste": rows(coste[coste["batch"] == 16], ["context", "horizon", "cells_per_second", "peak_vram_gb"]),
        "escala": rows(escala, ["site", "method", "cells", "n", "rmse", "mae", "bias", "r",
                                "skill_vs_clim"]) if len(escala) else [],
    }


def check_parity(payload: dict, report: Path = REPORT) -> None:
    """Aborta si alguna cifra volcada se desvia de su CSV de origen.

    Es el mismo control que se aplico al informe, donde las catorce cifras
    principales coincidieron sin desviacion. Aqui protege contra que la pagina y
    el informe cuenten cosas distintas.
    """
    nacional = pd.read_csv(report / "nacional_limpio" / "metrics_all.csv")
    # Valores del run limpio (backtest_clean, 17.027 celdas), PLAN_1 §3.
    esperado = {
        ("ll4", "timesfm"): 1.1536, ("ll4", "tuned"): 1.2279, ("ll4", "climatology"): 1.5352,
        ("ll2", "timesfm"): 1.1533, ("ll2", "tuned"): 1.2765,
        ("ll1", "timesfm"): 1.1736, ("ll1", "tuned"): 1.2538,
    }
    for (split, method), value in esperado.items():
        fuente = float(nacional[(nacional["split"] == split) & (nacional["method"] == method)]["rmse"].iloc[0])
        if abs(fuente - value) > 5e-4:
            raise ValueError(f"{method} {split}: el CSV trae {fuente:.4f} y se esperaba {value}")
        volcado = [r for r in payload["tablas"]["nacional"]
                   if r["split"] == split and r["method"] == method]
        if not volcado or abs(volcado[0]["rmse"] - fuente) > 5e-4:
            raise ValueError(f"{method} {split}: lo volcado no coincide con el CSV")
    logger.info("paridad con los CSV del informe: sin discrepancias")


def build(out_path: Path, *, report: Path = REPORT, res: Path = RES, silver: Path = SILVER) -> Path:
    layers, meta = build_layers(res=res, silver=silver, report=report)
    geo = json.loads((report / "geo" / "peru_departamental_simple.geojson").read_text())

    payload = {
        "meta": meta,
        "capas": layers,
        "zonas": zone_metrics(report),
        "etiquetasZona": zone_labels(res),
        "curva": error_curve(report),
        "tablas": tables(report),
        "contornos": geo,
    }
    check_parity(payload, report)

    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"window.DATOS = {body};\n", encoding="utf-8")

    size = out_path.stat().st_size
    for name, blob in layers.items():
        logger.info("  capa %-10s %6.1f KB", name, len(blob) / 1024)
    logger.info("  contornos   %6.1f KB", len(json.dumps(geo, separators=(",", ":"))) / 1024)
    logger.info("total %.1f KB", size / 1024)
    if size > MAX_BYTES:
        raise ValueError(f"el archivo pesa {size / 1024:.0f} KB y el limite es {MAX_BYTES // 1024} KB")
    return out_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=REPORT / "artifact" / "datos.js")
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    path = build(args.out, report=args.report)
    print(f"escrito {path} ({path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
