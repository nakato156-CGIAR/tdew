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

from . import paths

logger = logging.getLogger("timesfm.artifact")

REPORT = Path("reports/timesfm_benchmark")
SILVER = Path("Data/silver")
RES = paths.RES

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

# Producto completo 2017-2020 (E9): salidas de real_compare y real_tail.
CAMPO = "real_limpio"
AGG_REAL = paths.WORK / "agg_real"
MANIFIESTO_REAL = paths.WORK / "preds_real/MANIFEST.csv"
CAMPO_CELDAS = 2_178_827
CAMPO_VALORES = 3_183_266_247
TASA_COLA = 35.0
# Cantidades del control de reproduccion de Palacios que no coinciden con el paper (el texto de la
# pagina lo dice; si cambian, la pagina deja de ser cierta y hay que reescribirla).
CONTROL_FALLAN: frozenset[str] = frozenset()
# Cola calida de Palacios en el paper (sec-results-tail, tbl-support): celdas afectadas por nivel de
# soporte, total de celdas, porcentaje de valores sobre 35 C y maximo.
PAPER_COLA = {"celdas_por_tier": {"within": 0, "near": 10, "marginal": 391, "extrapolated": 18888,
                                  "unsupported": 113631},
              "celdas": 132920, "pct": 0.1326, "max": 41.16}


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
    # El producto 2017-2020 es la cobertura mas extensa de todas: TimesFM reconstruyo
    # cada celda del producto de Palacios, que abarca todo el Peru. Se pinta antes
    # que la pasada de escala (codigo 5) y las dos se solapan.
    campo_path = AGG_REAL / "agreement_by_cell_limpio.csv"
    n_campo = 0
    if campo_path.exists():
        campo_ids = pd.read_csv(campo_path, usecols=["ID"])["ID"].to_numpy(np.int64)
        sample[campo_ids] = 5
        n_campo = int((sample == 5).sum())
        if n_campo != CAMPO_CELDAS:
            raise ValueError(f"el campo 2017-2020 cubre {n_campo} celdas y se esperaban {CAMPO_CELDAS}")
    logger.info("campo 2017-2020: %d celdas", n_campo)

    escala_path = paths.WORK / "panel_436k.csv"
    n_escala = 0
    if escala_path.exists():
        escala_ids = pd.read_csv(escala_path)["ID"].to_numpy()
        sample[escala_ids] = 4
        n_escala = len(np.unique(escala_ids))
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
    panel_path = paths.RECONSTRUCTION_WORK / "panels/ll4_reducido_512.csv"
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
        "campoCeldas": n_campo,
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


SOPORTE_COLUMNS = ("split", "tier", "method", "cells", "n", "rmse", "mae", "bias", "r", "skill")
MENSUAL_COLUMNS = ("split", "method", "month", "bias_pooled", "n", "cells",
                   "cell_bias_std", "cell_bias_p05", "cell_bias_p95")
_INT_COLUMNS = {"cells", "n", "month"}


def _records(frame: pd.DataFrame, columns: Sequence[str]) -> list[dict]:
    """Filas listas para JSON estricto: enteros como int, NaN como null (``None``),
    flotantes a seis decimales. ``json.dumps`` con NaN no es JSON valido. Seis y no
    cuatro porque la pagina resta RMSE ya volcados (ΔRMSE por tier): con cuatro
    decimales 0.9464 − 0.8669 da 0.0795 y se mostraria 0.080 en vez de 0.079."""
    out = []
    for raw in frame.to_dict("records"):
        row = {}
        for c in columns:
            v = raw[c]
            if isinstance(v, str):
                row[c] = v
            elif pd.isna(v):
                row[c] = None
            elif c in _INT_COLUMNS:
                row[c] = int(v)
            else:
                row[c] = round(float(v), 6)
        out.append(row)
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

    soporte = pd.read_csv(report / "nacional_limpio" / "tiers_limpio.csv")
    mensual = pd.read_csv(report / "nacional_limpio" / "sesgo_mensual_limpio.csv")

    dept_pooled = dept[dept["level"] == "pooled"]
    dept_por = dept[dept["level"] == "department"]

    return {
        "nacional": rows(nacional, ["split", "method", "n", "rmse", "mae", "bias", "r", "skill_vs_clim"]),
        "soporte": _records(soporte, SOPORTE_COLUMNS),
        "sesgoMensual": _records(mensual, MENSUAL_COLUMNS),
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


# Cifras de PLAN_2 (run limpio, ll4): las de tbl-tiers del paper para ``tuned`` y las
# de TimesFM de reports/timesfm_benchmark/README.md.
TIER_CELLS = {"within": 8306, "near": 1779, "marginal": 1433, "extrapolated": 2563,
              "unsupported": 2946}
TIER_RMSE_EXPECTED = {
    "tuned": {"within": 0.946, "near": 1.139, "marginal": 1.276, "extrapolated": 1.374,
              "unsupported": 1.724},
    "timesfm": {"within": 0.867, "near": 1.061, "marginal": 1.198, "extrapolated": 1.298,
                "unsupported": 1.652},
}
MONTH_BIAS_EXPECTED = {("tuned", 12): 0.017, ("tuned", 1): -0.402, ("timesfm", 1): -0.325,
                       ("timesfm", 12): 0.089}


def _check_parity_tier_month(payload: dict, report: Path) -> None:
    """Soporte observacional y sesgo mensual: lo volcado es el CSV, fila por fila, y
    las cifras clave coinciden con las del informe y las del paper."""
    for key, csv, columns, keys in (
        ("soporte", "tiers_limpio.csv", SOPORTE_COLUMNS, ("split", "tier", "method")),
        ("sesgoMensual", "sesgo_mensual_limpio.csv", MENSUAL_COLUMNS, ("split", "method", "month")),
    ):
        fuente = pd.read_csv(report / "nacional_limpio" / csv)
        volcado = payload["tablas"][key]
        if len(volcado) != len(fuente):
            raise ValueError(f"{key}: se volcaron {len(volcado)} filas y el CSV trae {len(fuente)}")
        index = {tuple(r[k] for k in keys): r for r in volcado}
        for raw in fuente.to_dict("records"):
            row = index.get(tuple(raw[k] if k != "month" else int(raw[k]) for k in keys))
            if row is None:
                raise ValueError(f"{key}: falta la fila {[raw[k] for k in keys]}")
            for c in columns:
                if c in keys:
                    continue
                esperado = None if pd.isna(raw[c]) else float(raw[c])
                if (esperado is None) != (row[c] is None) or (
                        esperado is not None and abs(row[c] - esperado) > 1e-5):
                    raise ValueError(f"{key} {[raw[k] for k in keys]} {c}: {row[c]} != {esperado}")

    ll4 = {(r["tier"], r["method"]): r for r in payload["tablas"]["soporte"] if r["split"] == "ll4"}
    for tier, cells in TIER_CELLS.items():
        if ll4[(tier, "tuned")]["cells"] != cells:
            raise ValueError(f"{tier}: {ll4[(tier, 'tuned')]['cells']} celdas, se esperaban {cells}")
    for method, by_tier in TIER_RMSE_EXPECTED.items():
        for tier, value in by_tier.items():
            if abs(ll4[(tier, method)]["rmse"] - value) > 5e-4:
                raise ValueError(f"RMSE {method} {tier}: {ll4[(tier, method)]['rmse']} != {value}")
    mensual = {(r["method"], r["month"]): r for r in payload["tablas"]["sesgoMensual"]
               if r["split"] == "ll4"}
    for (method, month), value in MONTH_BIAS_EXPECTED.items():
        # 1e-3: el valor se cita a tres decimales (diciembre de tuned es 0.01748,
        # que se cita como +0.017).
        if abs(mensual[(method, month)]["bias_pooled"] - value) > 1e-3:
            raise ValueError(f"sesgo {method} mes {month}: "
                             f"{mensual[(method, month)]['bias_pooled']} != {value}")


# ----------------------------------------------------------------- campo 2017-2020

def _campo_csv(report: Path, name: str) -> pd.DataFrame:
    return pd.read_csv(report / CAMPO / f"{name}_limpio.csv")


def _plain(frame: pd.DataFrame) -> list[dict]:
    """Todas las columnas tal como estan en el CSV: texto, booleanos y enteros intactos,
    NaN como ``None`` y flotantes a seis decimales (ver ``_records``)."""
    out = []
    for raw in frame.to_dict("records"):
        row = {}
        for k, v in raw.items():
            if isinstance(v, str):
                row[k] = v
            elif isinstance(v, (bool, np.bool_)):
                row[k] = bool(v)
            elif isinstance(v, (int, np.integer)):
                row[k] = int(v)
            elif pd.isna(v):
                row[k] = None
            else:
                row[k] = round(float(v), 6)
        out.append(row)
    return out


def _dia(series: pd.DataFrame, col: str, how: str) -> dict:
    i = getattr(series[col], how)()
    return {"fecha": str(series["date"].loc[i]), "valor": float(series[col].loc[i])}


def cola_razones(cola: dict) -> dict:
    """Cocientes TimesFM / Palacios de la cola, para el texto de la pagina (se calculan aqui, no en el navegador)."""
    r = {x["product"]: x for x in cola["resumen"]}
    out = {"tasa_35": (r["timesfm"]["above_35"] / r["timesfm"]["n"]) / (r["palacios"]["above_35"] / r["palacios"]["n"]),
           "celdas": r["timesfm"]["cells_with_exceedance"] / r["palacios"]["cells_with_exceedance"],
           "sobre_38": r["timesfm"]["above_38"] / r["palacios"]["above_38"], "noviembre": {}}
    for k in ("timesfm", "palacios"):
        mes = [x for x in cola["mes"] if x["product"] == k and x["zone_class"] == "selva_A(r)A'"]
        total = sum(x["above_35"] for x in mes)
        out["noviembre"][k] = sum(x["above_35"] for x in mes if x["month"] == 11) / total if total else None
        tiers = [x for x in cola["tier"] if x["product"] == k and x["tier"] != "within"]
        out.setdefault("fuera_dominio", {})[k] = (sum(x["above_35"] for x in tiers) / sum(x["values"] for x in tiers) * 100)
    return out


def anomalia_estadisticos(series: pd.DataFrame) -> dict:
    """Cifras de la serie diaria de anomalia nacional de cada producto (promedio sobre las celdas).

    Se calculan aqui, no en el navegador: la pagina no recalcula nada.
    """
    t, p = series["anom_timesfm"], series["anom_palacios"]
    top, bot = p >= p.quantile(0.95), p <= p.quantile(0.05)
    return {
        "dias": int(len(series)),
        "r": float(t.corr(p)),
        "desv_timesfm": float(t.std()), "desv_palacios": float(p.std()),
        "cociente_desv": float(t.std() / p.std()),
        "media_timesfm": float(t.mean()), "media_palacios": float(p.mean()),
        "acuerdo_signo": float(((t > 0) == (p > 0)).mean()),
        "extremos_calidos": {"n": int(top.sum()), "palacios": float(p[top].mean()), "timesfm": float(t[top].mean())},
        "extremos_frios": {"n": int(bot.sum()), "palacios": float(p[bot].mean()), "timesfm": float(t[bot].mean())},
        "dif_media": float((t - p).mean()), "dif_desv": float((t - p).std()),
        "dia_mas_calido": {k: _dia(series, col, "idxmax") for k, col in (("palacios", "anom_palacios"), ("timesfm", "anom_timesfm"))},
        "dia_mas_frio": {k: _dia(series, col, "idxmin") for k, col in (("palacios", "anom_palacios"), ("timesfm", "anom_timesfm"))},
    }


def cola_layer(agg: Path = AGG_REAL) -> tuple[str, dict]:
    """Capa del mapa de la cola calida: por celda, 1 solo TimesFM, 2 solo Palacios, 3 ambos.

    El ``ID`` es denso y en orden row-major, igual que en el resto de las capas.
    """
    cells = pd.read_csv(agg / "tail_by_cell_limpio.csv")
    t, p = cells["n_above_timesfm"].to_numpy() > 0, cells["n_above_palacios"].to_numpy() > 0
    ids = cells["ID"].to_numpy(np.int64)
    layer = np.zeros(N_LAT * N_LON, dtype=np.uint8)
    layer[ids[t & ~p]], layer[ids[~t & p]], layer[ids[t & p]] = 1, 2, 3
    counts = {"solo_timesfm": int((t & ~p).sum()), "solo_palacios": int((~t & p).sum()),
              "ambos": int((t & p).sum())}
    return encode(layer), counts


def campo(report: Path = REPORT, agg: Path = AGG_REAL, manifest: Path = MANIFIESTO_REAL) -> dict:
    """Producto completo 2017-2020: acuerdo entre productos, anomalia y cola calida."""
    serie = _campo_csv(report, "anomaly_series")
    man = pd.read_csv(manifest) if manifest.exists() else None
    manifiesto = None
    if man is not None:
        seconds = float(man["seconds"].sum())
        manifiesto = {"buckets": int(len(man)), "celdas": int(man["cells_written"].sum()),
                      "omitidas": int(man["n_omitted"].sum()), "filas": int(man["rows"].sum()),
                      "bytes": int(man["bytes"].sum()), "segundos": seconds,
                      "celdas_por_s": float(man["cells_written"].sum() / seconds),
                      "violaciones_cuantiles": int(man["quantile_violation_rows"].sum())}
    capa, conteos = cola_layer(agg)
    out = {
        "manifiesto": manifiesto,
        "producto": _plain(_campo_csv(report, "product_figures")),
        "control": _plain(_campo_csv(report, "reproduction_palacios")),
        "acuerdo": {
            "global": _plain(_campo_csv(report, "agreement_overall"))[0],
            "anio": _plain(_campo_csv(report, "agreement_by_year")),
            "tier": _plain(_campo_csv(report, "agreement_by_tier")),
            "sitio": _plain(_campo_csv(report, "agreement_by_site")),
            "mes": _plain(_campo_csv(report, "agreement_by_month")),
        },
        "deriva": _plain(_campo_csv(report, "drift")),
        "anomalia": {
            "inicio": str(serie["date"].iloc[0]),
            "timesfm": [round(float(v), 3) for v in serie["anom_timesfm"]],
            "palacios": [round(float(v), 3) for v in serie["anom_palacios"]],
            "td_timesfm": [round(float(v), 3) for v in serie["mean_timesfm"]],
            "td_palacios": [round(float(v), 3) for v in serie["mean_palacios"]],
            "clim": [round(float(v), 3) for v in serie["clim_mean"]],
            "estadisticos": anomalia_estadisticos(serie),
        },
        "cola": {
            "resumen": _plain(_campo_csv(report, "tail_summary")),
            "tier": _plain(_campo_csv(report, "tail_by_tier")),
            "zona": _plain(_campo_csv(report, "tail_by_zone_class")),
            "mes": _plain(_campo_csv(report, "tail_by_month")),
            "anio": _plain(_campo_csv(report, "tail_by_year")),
            "solape": _plain(_campo_csv(report, "tail_joint")),
            "supervivencia": _plain(_campo_csv(report, "tail_survival")),
            "celdas": conteos,
            "capa": capa,
        },
    }
    out["cola"]["razones"] = cola_razones(out["cola"])
    return out


def check_parity_campo(payload: dict, report: Path = REPORT) -> None:
    """Aborta si el campo volcado no coincide con sus CSV o si las tablas no cuadran entre si."""
    c = payload["campo"]
    for fila in c["producto"]:
        if fila["cells"] != CAMPO_CELDAS or fila["n"] != CAMPO_VALORES:
            raise ValueError(f"{fila['product']}: {fila['cells']} celdas y {fila['n']} valores; "
                             f"se esperaban {CAMPO_CELDAS} y {CAMPO_VALORES}")
    resumen = {r["product"]: r for r in c["cola"]["resumen"]}
    for name, r in resumen.items():
        if r["n"] != CAMPO_VALORES or r["cells"] != CAMPO_CELDAS:
            raise ValueError(f"cola {name}: {r['n']} valores y {r['cells']} celdas")
        tier = [x for x in c["cola"]["tier"] if x["product"] == name]
        if sum(x["cells"] for x in tier) != CAMPO_CELDAS or sum(x["values"] for x in tier) != CAMPO_VALORES:
            raise ValueError(f"cola {name}: las celdas o valores por tier no suman el total")
        if sum(x["above_35"] for x in tier) != r["above_35"]:
            raise ValueError(f"cola {name}: lo que supera 35 C por tier no suma el total")
        zona = [x for x in c["cola"]["zona"] if x["product"] == name]
        if sum(x["above_35"] for x in zona) != r["above_35"]:
            raise ValueError(f"cola {name}: lo que supera 35 C por clase no suma el total")
        mes = [x for x in c["cola"]["mes"] if x["product"] == name and x["zone_class"] == "todo"]
        anio = [x for x in c["cola"]["anio"] if x["product"] == name]
        if sum(x["above_35"] for x in mes) != r["above_35"] or sum(x["above_35"] for x in anio) != r["above_35"]:
            raise ValueError(f"cola {name}: lo que supera 35 C por mes o por anio no suma el total")
    pal = resumen["palacios"]
    for x in c["cola"]["tier"]:
        if x["product"] == "palacios" and x["cells_affected"] != PAPER_COLA["celdas_por_tier"][x["tier"]]:
            raise ValueError(f"Palacios {x['tier']}: {x['cells_affected']} celdas afectadas y el paper dice "
                             f"{PAPER_COLA['celdas_por_tier'][x['tier']]}")
    if (pal["cells_with_exceedance"] != PAPER_COLA["celdas"] or round(pal["pct_above_35"], 4) != PAPER_COLA["pct"]
            or round(pal["max"], 2) != PAPER_COLA["max"]):
        raise ValueError(f"la cola de Palacios no reproduce el paper: {pal['cells_with_exceedance']} celdas, "
                         f"{pal['pct_above_35']:.4f} %, maximo {pal['max']:.2f}")
    capa = c["cola"]["celdas"]
    for name, key in (("timesfm", "solo_timesfm"), ("palacios", "solo_palacios")):
        con = capa[key] + capa["ambos"]
        if con != resumen[name]["cells_with_exceedance"]:
            raise ValueError(f"cola {name}: el mapa tiene {con} celdas afectadas y el resumen "
                             f"{resumen[name]['cells_with_exceedance']}")
    if payload["campo"]["acuerdo"]["global"]["n"] != CAMPO_VALORES:
        raise ValueError("el acuerdo global no cubre los 3 183 266 247 valores")
    fallan = {r["quantity"] for r in c["control"] if not r["ok"]}
    if fallan != CONTROL_FALLAN:
        raise ValueError(f"control de reproduccion: fallan {sorted(fallan)} y el texto de la pagina dice "
                         f"{sorted(CONTROL_FALLAN)}")
    if len(c["anomalia"]["timesfm"]) != 1461 or len(c["anomalia"]["palacios"]) != 1461:
        raise ValueError("la serie de anomalia no tiene 1 461 dias")
    if c["manifiesto"] is not None:
        m = c["manifiesto"]
        if (m["buckets"], m["celdas"], m["omitidas"], m["filas"]) != (8192, CAMPO_CELDAS, 0, CAMPO_VALORES):
            raise ValueError(f"el manifiesto no cuadra con el producto esperado: {m}")
    logger.info("paridad del campo 2017-2020: sin discrepancias")


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
    _check_parity_tier_month(payload, report)
    logger.info("paridad con los CSV del informe: sin discrepancias")


KL_DIR = "kl_limpio"


def kl_layer(report: Path = REPORT) -> dict:
    """Divergencia KL del backtest limpio: tabla por grupo y densidades de Td en bins de 0,5 C.

    Las contribuciones por bin se recalculan aqui desde las cuentas con el mismo suavizado de
    ``kl.divergences``; ``check_parity_kl`` comprueba que suman la KL del CSV.
    """
    from .kl import ALPHA, METHODS

    grupos = pd.read_csv(report / KL_DIR / "kl_by_group_limpio.csv")
    hist = pd.read_csv(report / KL_DIR / "kl_hist_limpio.csv")
    p = hist["obs"].to_numpy(dtype=float) + ALPHA
    p = p / p.sum()
    bins = {"lo": [round(float(v), 6) for v in hist["bin_lo"]], "hi": [round(float(v), 6) for v in hist["bin_hi"]],
            "obs": [round(float(v), 8) for v in p]}
    for method in METHODS:
        q = hist[method].to_numpy(dtype=float) + ALPHA
        q = q / q.sum()
        bins[method] = [round(float(v), 8) for v in q]
        bins[f"aporte_{method}"] = [round(float(v), 8) for v in p * np.log(p / q)]
    return {"grupos": _plain(grupos), "bins": bins, "alpha": ALPHA,
            "n": int(grupos.loc[(grupos.group == "todo") & (grupos.bin_width == 0.5), "n"].iloc[0])}


def check_parity_kl(payload: dict, report: Path = REPORT) -> None:
    kl = payload["kl"]
    csv = pd.read_csv(report / KL_DIR / "kl_by_group_limpio.csv")
    problems = []
    for method in ("palacios", "timesfm"):
        row = csv[(csv.group_kind == "todo") & (csv.method == method) & (csv.bin_width == 0.5)]
        suma = float(np.sum(kl["bins"][f"aporte_{method}"]))
        esperado = float(row["kl_obs_method"].iloc[0])
        if abs(suma - esperado) > 1e-6:
            problems.append(f"{method}: la suma de aportes {suma:.8f} no coincide con la KL {esperado:.8f}")
    if len(kl["grupos"]) != len(csv):
        problems.append(f"filas de grupos {len(kl['grupos'])} frente a {len(csv)}")
    for name in ("obs", "palacios", "timesfm"):
        total = float(np.sum(kl["bins"][name]))
        if abs(total - 1.0) > 1e-5:
            problems.append(f"la densidad {name} suma {total}")
    if problems:
        raise ValueError("paridad de KL: " + "; ".join(problems))
    logger.info("paridad de KL: sin discrepancias")


def build(out_path: Path, *, report: Path = REPORT, res: Path = RES, silver: Path = SILVER,
          with_campo: bool = True, agg: Path = AGG_REAL) -> Path:
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
    if with_campo:
        payload["campo"] = campo(report, agg)
    if (report / KL_DIR / "kl_by_group_limpio.csv").exists():
        payload["kl"] = kl_layer(report)
    check_parity(payload, report)
    if "kl" in payload:
        check_parity_kl(payload, report)
    if with_campo:
        check_parity_campo(payload, report)

    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"window.DATOS = {body};\n", encoding="utf-8")

    size = out_path.stat().st_size
    for name, blob in layers.items():
        logger.info("  capa %-10s %6.1f KB", name, len(blob) / 1024)
    if with_campo:
        logger.info("  capa %-10s %6.1f KB", "cola", len(payload["campo"]["cola"]["capa"]) / 1024)
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
