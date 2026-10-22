"""Divergencia calida de Td (backtest limpio 2013-2016): ¿se concentra en zonas o en anios?

El histograma nacional de ``kl.py`` muestra que TimesFM y Palacios (LLR, ``pred_tuned``)
ponen poca masa entre 20 y 24 C y demasiada entre 24,5 y 27 C. Aqui se corta esa senal
por zona SENAMHI, banda de altitud, departamento, nivel de soporte, anio, mes y anio-mes,
para los tres metodos (TimesFM, LLR y la climatologia ``pred_clim`` como referencia).

Por grupo g y metodo m, con B = [20, 24) y B' = [24,5, 27]:

- ``delta_B = P_pred(B) - P_obs(B)`` (masa relativa al total del grupo); igual para B'.
- ``share_B = n_g * delta_B / suma nacional de n * delta``: fraccion del deficit nacional
  que aporta el grupo. En un corte que particiona las filas, los ``share`` suman 1.
- ``kl_B``: contribucion de los bins de B a KL(obs || metodo) dentro del grupo, con la
  formula y el suavizado de ``kl.divergences`` en bins de 0,5 C.
- ``bias_obs_B = mean(pred - obs | obs en B)`` y ``bias_pred_Bp = mean(obs - pred | pred en B')``:
  separan la regresion a la media (suavizar el extremo calido) de un desplazamiento.

El corte zona x anio se limita a las zonas que, ordenadas por ``share_B`` de TimesFM, suman
~80 % del deficit nacional en B; las mismas zonas valen para los tres metodos. Para delta_B
por zona y por anio se dan IC 95 % por bootstrap de bloques (2 grados y mes-anio, como en
``experiments.amenazas.desglose``), remuestreando conteos agregados por bloque.

Uso: ``uv run python -m experiments.timesfm.kl_calido [--limit-ids N] [--n-boot 200]``
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from dataclasses import replace
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from experiments.amenazas.desglose import BLOCK_DEG, block_keys
from tdew_estimation import provenance as prov

from . import paths
from .kl import ALPHA, BIN_COARSE, HI, LO, _edges, _hist
from .kl import build_provenance as _kl_provenance
from .real import refuse_under_res
from .real_compare import DEFAULT_SUPPORT, DEFAULT_ZONE

logger = logging.getLogger(__name__)

DEFAULT_PALACIOS = paths.RES / "tuning/backtest_clean/ll4/predictions.parquet"
DEFAULT_TFM = paths.WORK / "preds_nacional/ll4__tmin_anom_full.parquet"
DEFAULT_STATIC = Path("Data/silver/static_covariates.parquet")
DEFAULT_GEO = Path("reports/timesfm_benchmark/geo/peru_departamental_simple.geojson")
DEFAULT_OUT = Path("reports/timesfm_benchmark/kl_calido")
# Columna del parquet -> nombre del metodo. El orden fija el orden de las tablas.
MODELS = {"pred": "timesfm", "pred_tuned": "llr", "pred_clim": "clim"}
B_LO, B_HI = 20.0, 24.0          # B = [20, 24)
BP_LO, BP_HI = 24.5, 27.0        # B' = [24,5, 27]
DEM_EDGES = (0.0, 500.0, 1500.0, 2500.0, 3500.0)
DEM_LABELS = ("0-500", "500-1500", "1500-2500", "2500-3500", ">3500")
COVER = 0.80
N_BOOT = 200
SEED = 0
CUTS = ("zona", "dem", "depto", "tier", "anio", "mes", "anio_mes", "zona_anio")
FIG_RANGE = (15.0, 28.0)
COLORS = {"obs": "#383835", "timesfm": "#2a78d6", "llr": "#eb6834", "clim": "#1baf7a"}


def _bin_index(values: np.ndarray, width: float = BIN_COARSE) -> np.ndarray:
    """Indice de bin con la misma aritmetica que ``kl._hist`` (bins extremos pliegan lo de fuera)."""
    clipped = np.clip(values, LO, np.nextafter(HI, LO))
    return np.floor((clipped - LO) / width).astype(np.int16)


def b_bins(width: float = BIN_COARSE) -> np.ndarray:
    """Bins cuyo intervalo cae dentro de B."""
    lo = _edges(width)[:-1]
    return np.flatnonzero((lo >= B_LO - 1e-9) & (lo < B_HI - 1e-9))


# --------------------------------------------------------------------------- carga

def sample_ids(palacios: Path, n: int, seed: int = SEED) -> np.ndarray:
    ids = np.unique(pq.ParquetFile(palacios).read(columns=["ID"]).column("ID").to_numpy())
    return np.sort(np.random.default_rng(seed).choice(ids, size=min(n, len(ids)), replace=False))


def load_pairs(palacios: Path, tfm: Path, ids: np.ndarray | None = None) -> pd.DataFrame:
    """Pares (ID, FECHA) comunes con el filtro de ``kl.load_pairs`` (obs, LLR y TimesFM presentes).

    Se conservan los tipos de origen para que el histograma nacional reproduzca ``kl.py`` bin a bin.
    """
    filters = None if ids is None else [("ID", "in", [int(i) for i in ids])]
    pal = pq.read_table(palacios, columns=["ID", "zone_id", "FECHA", "TD_obs", "pred_tuned", "pred_clim"],
                        filters=filters).to_pandas()
    tf = pq.read_table(tfm, columns=["ID", "FECHA", "pred"], filters=filters).to_pandas()
    frame = pal.merge(tf, on=["ID", "FECHA"], how="inner", validate="one_to_one")
    logger.info("pares de Palacios %d, de TimesFM %d, comunes %d", len(pal), len(tf), len(frame))
    del pal, tf
    frame = frame.rename(columns={"TD_obs": "obs", **MODELS})
    frame = frame.dropna(subset=["obs", "llr", "timesfm"]).reset_index(drop=True)
    logger.info("tras el filtro: %d pares; clim sin valor en %d", len(frame), int(frame["clim"].isna().sum()))
    frame["year"] = frame["FECHA"].dt.year.astype(np.int16)
    frame["month"] = frame["FECHA"].dt.month.astype(np.int8)
    frame["zone_id"] = frame["zone_id"].astype(np.int32)
    return frame.drop(columns="FECHA")


def departments(lon: np.ndarray, lat: np.ndarray, geo: Path = DEFAULT_GEO) -> np.ndarray:
    """``NOMBDEP`` del departamento que contiene cada punto, o ``fuera_peru`` (patron de ``peru_mask``)."""
    import shapely
    from shapely.geometry import shape

    out = np.full(len(lon), "fuera_peru", dtype=object)
    for feat in json.loads(Path(geo).read_text())["features"]:
        poly = shape(feat["geometry"])
        shapely.prepare(poly)
        out[shapely.contains_xy(poly, lon, lat) & (out == "fuera_peru")] = feat["properties"]["NOMBDEP"]
    return out


def dem_band(dem: np.ndarray) -> np.ndarray:
    idx = np.searchsorted(np.asarray(DEM_EDGES[1:]), dem, side="right")
    out = np.asarray(DEM_LABELS, dtype=object)[np.clip(idx, 0, len(DEM_LABELS) - 1)]
    out[~np.isfinite(dem)] = "sin_dem"
    return out


def cell_table(ids: np.ndarray, zone_table: Path, support: Path, static: Path, geo: Path) -> pd.DataFrame:
    """Atributos por celda (una fila por ID unico): zona, lon/lat, tier, banda DEM y departamento."""
    cells = pd.DataFrame({"ID": ids})
    zt = pd.read_parquet(zone_table, columns=["ID", "zone_label", "lon", "lat"], filters=[("ID", "in", ids.tolist())])
    sd = pd.read_parquet(support, columns=["ID", "tier"], filters=[("ID", "in", ids.tolist())])
    st = pd.read_parquet(static, columns=["ID", "DEM"], filters=[("ID", "in", ids.tolist())])
    cells = cells.merge(zt, on="ID", how="left").merge(sd, on="ID", how="left").merge(st, on="ID", how="left")
    cells["tier"] = cells["tier"].fillna("desconocido")
    cells["dem_band"] = dem_band(cells["DEM"].to_numpy("f8"))
    cells["depto"] = departments(cells["lon"].to_numpy(), cells["lat"].to_numpy(), geo)
    cells["block_2g"] = block_keys(cells, "espacial_2g")
    return cells


# --------------------------------------------------------------------------- metricas

def _row_arrays(frame: pd.DataFrame, models: Sequence[str]) -> dict:
    """Indicadores por fila que comparten todos los cortes (se calculan una vez)."""
    obs = frame["obs"].to_numpy()
    arr = {"obs_bin": _bin_index(obs), "obs_in_B": (obs >= B_LO) & (obs < B_HI),
           "obs_in_Bp": (obs >= BP_LO) & (obs <= BP_HI)}
    for m in models:
        pred = frame[m].to_numpy()
        valid = ~np.isnan(pred)
        arr[m] = {"valid": valid, "bin": _bin_index(np.where(valid, pred, 0.0)),
                  "in_B": valid & (pred >= B_LO) & (pred < B_HI),
                  "in_Bp": valid & (pred >= BP_LO) & (pred <= BP_HI),
                  "err": np.where(valid, pred.astype("f8") - obs.astype("f8"), 0.0)}
    return arr


def _count(codes: np.ndarray, n: int, weights: np.ndarray | None = None) -> np.ndarray:
    return np.bincount(codes, weights=weights, minlength=n)[:n].astype("f8")


def group_metrics(codes: np.ndarray, n_groups: int, arr: Mapping, models: Sequence[str],
                  national: Mapping[str, tuple[float, float]], width: float = BIN_COARSE,
                  alpha: float = ALPHA) -> pd.DataFrame:
    """Metricas de banda por grupo y metodo. ``codes`` < 0 excluye la fila.

    ``national[m]`` = (suma nacional de n*delta_B, idem B') para m; es el denominador de
    ``share``, de modo que los ``share`` de una particion suman 1.
    """
    keep = codes >= 0
    c = codes[keep].astype(np.int64)
    nb = len(_edges(width)) - 1
    bins_b = b_bins(width)
    obs_bin = arr["obs_bin"][keep].astype(np.int64)
    rows = []
    for m in models:
        a = arr[m]
        v = a["valid"][keep]
        cv = np.where(v, c, n_groups)  # filas sin prediccion van a un grupo basura
        n = _count(cv, n_groups)
        o_b = _count(cv, n_groups, arr["obs_in_B"][keep])
        o_bp = _count(cv, n_groups, arr["obs_in_Bp"][keep])
        p_b = _count(cv, n_groups, a["in_B"][keep])
        p_bp = _count(cv, n_groups, a["in_Bp"][keep])
        err = a["err"][keep]
        bias_b = _count(cv, n_groups, np.where(arr["obs_in_B"][keep], err, 0.0))
        bias_bp = _count(cv, n_groups, np.where(a["in_Bp"][keep], -err, 0.0))
        h_obs = _count(cv * nb + obs_bin, (n_groups + 1) * nb).reshape(-1, nb)[:n_groups]
        h_m = _count(cv * nb + a["bin"][keep].astype(np.int64), (n_groups + 1) * nb).reshape(-1, nb)[:n_groups]
        p = (h_obs + alpha) / (h_obs + alpha).sum(axis=1, keepdims=True)
        q = (h_m + alpha) / (h_m + alpha).sum(axis=1, keepdims=True)
        terms = p * np.log(p / q)
        nd_b, nd_bp = national[m]
        with np.errstate(invalid="ignore", divide="ignore"):
            rows.append(pd.DataFrame({
                "group_code": np.arange(n_groups), "model": m, "n": n.astype(np.int64),
                "n_obs_B": o_b.astype(np.int64),
                "p_obs_B": o_b / n, "p_pred_B": p_b / n, "delta_B": (p_b - o_b) / n,
                "share_B": (p_b - o_b) / nd_b if nd_b else np.nan,
                "p_obs_Bp": o_bp / n, "p_pred_Bp": p_bp / n, "delta_Bp": (p_bp - o_bp) / n,
                "share_Bp": (p_bp - o_bp) / nd_bp if nd_bp else np.nan,
                "kl_B": terms[:, bins_b].sum(axis=1), "kl_total": terms.sum(axis=1),
                "bias_obs_B": bias_b / o_b, "n_pred_Bp": p_bp.astype(np.int64),
                "bias_pred_Bp": bias_bp / p_bp,
            }))
    out = pd.concat(rows, ignore_index=True)
    return out[out["n"] > 0].reset_index(drop=True)


def national_totals(arr: Mapping, models: Sequence[str]) -> dict[str, tuple[float, float]]:
    """Suma nacional de n*delta (= cuentas pred en banda - cuentas obs en banda) por metodo."""
    out = {}
    for m in models:
        v = arr[m]["valid"]
        out[m] = (float(arr[m]["in_B"].sum() - (arr["obs_in_B"] & v).sum()),
                  float(arr[m]["in_Bp"].sum() - (arr["obs_in_Bp"] & v).sum()))
    return out


def block_weights(k: int, n_boot: int, seed: int = SEED) -> np.ndarray:
    """Pesos de remuestreo de ``k`` bloques con reemplazo, mismo esquema que ``desglose.block_bootstrap``."""
    rng = np.random.default_rng(seed)
    draws = rng.integers(0, k, size=(n_boot, k))
    w = np.zeros((n_boot, k))
    np.add.at(w, (np.repeat(np.arange(n_boot), k), draws.ravel()), 1.0)
    return w


def bootstrap_delta(n: np.ndarray, obs_in: np.ndarray, pred_in: Mapping[str, np.ndarray],
                    n_boot: int = N_BOOT, seed: int = SEED) -> dict[str, tuple[float, float]]:
    """IC 95 % de delta = (suma pred en banda - suma obs en banda) / suma n sobre bloques remuestreados.

    Entra un vector por bloque (no filas). Todos los metodos usan las mismas replicas.
    """
    k = len(n)
    if k < 2:
        return {m: (np.nan, np.nan) for m in pred_in}
    w = block_weights(k, n_boot, seed)
    big_n, big_o = w @ n, w @ obs_in
    out = {}
    for m, p in pred_in.items():
        with np.errstate(invalid="ignore", divide="ignore"):
            rep = (w @ p - big_o) / big_n
        lo, hi = np.nanpercentile(rep, [2.5, 97.5])
        out[m] = (float(lo), float(hi))
    return out


def group_ci(codes: np.ndarray, n_groups: int, blocks: np.ndarray, arr: Mapping, models: Sequence[str],
             n_boot: int, seed: int) -> pd.DataFrame:
    """IC de delta_B por grupo: se agregan conteos por (grupo, bloque) y se remuestrean los bloques del grupo."""
    _, bcode = np.unique(blocks, return_inverse=True)
    nbk = int(bcode.max()) + 1
    key = codes.astype(np.int64) * nbk + bcode
    rows = []
    for m in models:
        v = arr[m]["valid"]
        kv = np.where(v, key, -1)
        sel = kv >= 0
        uniq, inv = np.unique(kv[sel], return_inverse=True)
        n = _count(inv, len(uniq))
        o = _count(inv, len(uniq), arr["obs_in_B"][sel])
        p = _count(inv, len(uniq), arr[m]["in_B"][sel])
        grp = uniq // nbk
        for g in range(n_groups):
            idx = grp == g
            if not idx.any():
                continue
            lo, hi = bootstrap_delta(n[idx], o[idx], {m: p[idx]}, n_boot, seed)[m]
            rows.append({"group_code": g, "model": m, "n_blocks": int(idx.sum()), "lo": lo, "hi": hi})
    return pd.DataFrame(rows)


def _codes(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    cats, codes = np.unique(values, return_inverse=True)
    return codes.astype(np.int32), cats


def compute(frame: pd.DataFrame, cells: pd.DataFrame, models: Sequence[str] = tuple(MODELS.values()),
            n_boot: int = N_BOOT, seed: int = SEED, cover: float = COVER) -> dict[str, pd.DataFrame]:
    """Tablas por corte. ``cells`` es la tabla de ``cell_table`` con una fila por ID de ``frame``."""
    cells = cells.set_index("ID")
    cell_idx = np.searchsorted(cells.index.to_numpy(), frame["ID"].to_numpy())
    arr = _row_arrays(frame, models)
    national = national_totals(arr, models)
    year = frame["year"].to_numpy()
    month = frame["month"].to_numpy()
    blocks = {"espacial_2g": cells["block_2g"].to_numpy()[cell_idx],
              "mes_anio": block_keys(pd.DataFrame({"year": year, "month": month}), "mes_anio")}

    # zone_id viene por fila en las predicciones; su etiqueta, por celda en zone_table.
    first = np.unique(cell_idx, return_index=True)[1]
    zone_label = pd.Series(cells["zone_label"].to_numpy()[cell_idx[first]],
                           index=frame["zone_id"].to_numpy()[first]).groupby(level=0).first()

    specs: dict[str, tuple[np.ndarray, pd.DataFrame]] = {}
    zcode, zcats = _codes(frame["zone_id"].to_numpy())
    specs["zona"] = (zcode, pd.DataFrame({"zone_id": zcats, "zone_label": zone_label.reindex(zcats).to_numpy()}))
    for cut, col, name in (("dem", "dem_band", "dem_band"), ("depto", "depto", "depto"), ("tier", "tier", "tier")):
        cc, cats = _codes(cells[col].to_numpy().astype(str))
        specs[cut] = (cc[cell_idx], pd.DataFrame({name: cats}))
    ycode, ycats = _codes(year)
    specs["anio"] = (ycode, pd.DataFrame({"anio": ycats}))
    mcode, mcats = _codes(month)
    specs["mes"] = (mcode, pd.DataFrame({"mes": mcats}))
    ymcode, ymcats = _codes(year.astype(np.int32) * 100 + month)
    specs["anio_mes"] = (ymcode, pd.DataFrame({"anio": ymcats // 100, "mes": ymcats % 100}))

    tables: dict[str, pd.DataFrame] = {}
    for cut, (codes, labels) in specs.items():
        t = group_metrics(codes, len(labels), arr, models, national)
        if cut in ("zona", "anio"):
            for scheme, bk in blocks.items():
                ci = group_ci(codes, len(labels), bk, arr, models, n_boot, seed)
                ci = ci.rename(columns={"n_blocks": f"bloques_{scheme}", "lo": f"delta_B_lo_{scheme}",
                                        "hi": f"delta_B_hi_{scheme}"})
                t = t.merge(ci, on=["group_code", "model"], how="left")
        tables[cut] = _finish(t, labels, codes, cell_idx)
        logger.info("corte %s: %d grupos", cut, len(labels))

    # Zona x anio: zonas que suman ~cover del deficit nacional en B segun TimesFM.
    z = tables["zona"]
    ref = "timesfm" if "timesfm" in models else models[0]
    zs = z[z.model == ref].sort_values("share_B", ascending=False)
    cum = zs["share_B"].cumsum().to_numpy()
    n_sel = int(np.searchsorted(cum, cover) + 1) if len(cum) else 0
    chosen = zs["zone_id"].to_numpy()[:n_sel]
    logger.info("zonas que cubren %.0f %% del deficit (%s): %s", 100 * cover, ref, chosen.tolist())
    zsel = np.isin(zcats, chosen)
    zy = np.where(zsel[zcode], zcode.astype(np.int64) * len(ycats) + ycode, -1)
    zy_cats = np.arange(len(zcats) * len(ycats))
    labels = pd.DataFrame({"zone_id": zcats[zy_cats // len(ycats)],
                           "zone_label": zone_label.reindex(zcats[zy_cats // len(ycats)]).to_numpy(),
                           "anio": ycats[zy_cats % len(ycats)]})
    t = group_metrics(zy, len(labels), arr, models, national)
    t = _finish(t, labels, zy, cell_idx)
    order = {zid: i for i, zid in enumerate(chosen)}
    t = t.assign(_o=t["zone_id"].map(order)).sort_values(["_o", "anio", "model"]).drop(columns="_o")
    tables["zona_anio"] = t.reset_index(drop=True)
    return tables


def _finish(t: pd.DataFrame, labels: pd.DataFrame, codes: np.ndarray, cell_idx: np.ndarray) -> pd.DataFrame:
    """Une etiquetas y el numero de celdas por grupo; deja las etiquetas al frente."""
    keep = codes >= 0
    pairs = np.unique(codes[keep].astype(np.int64) * (int(cell_idx.max()) + 1) + cell_idx[keep])
    n_cells = np.bincount(pairs // (int(cell_idx.max()) + 1), minlength=len(labels))
    lab = labels.assign(group_code=np.arange(len(labels)), n_cells=n_cells[:len(labels)])
    t = lab.merge(t, on="group_code", how="inner").drop(columns="group_code")
    order = {m: i for i, m in enumerate(MODELS.values())}
    return t.assign(_m=t["model"].map(order)).sort_values([*labels.columns, "_m"]).drop(columns="_m").reset_index(drop=True)


def national_hist(frame: pd.DataFrame, models: Sequence[str] = tuple(MODELS.values())) -> pd.DataFrame:
    """Histograma nacional en bins de 0,5 C con ``kl._hist`` (comparable con ``kl_hist_limpio.csv``)."""
    edges = _edges(BIN_COARSE)
    hist = {"bin_lo": edges[:-1], "bin_hi": edges[1:]}
    for col in ("obs", *models):
        vals = frame[col].to_numpy()
        hist[col], _ = _hist(vals[~np.isnan(vals)], BIN_COARSE)
    hist = pd.DataFrame(hist)
    return hist[hist[["obs", *models]].sum(axis=1) > 0].reset_index(drop=True)


def cell_delta(frame: pd.DataFrame, models: Sequence[str] = ("timesfm", "llr")) -> pd.DataFrame:
    """delta_B por celda, agregando todas las fechas (para el mapa)."""
    ids, inv = np.unique(frame["ID"].to_numpy(), return_inverse=True)
    obs = frame["obs"].to_numpy()
    n = np.bincount(inv).astype("f8")
    o = np.bincount(inv, weights=(obs >= B_LO) & (obs < B_HI))
    out = pd.DataFrame({"ID": ids, "n": n})
    for m in models:
        p = frame[m].to_numpy()
        out[m] = (np.bincount(inv, weights=(p >= B_LO) & (p < B_HI)) - o) / n
    return out


# --------------------------------------------------------------------------- figuras

def make_figures(frame: pd.DataFrame, cells: pd.DataFrame, tables: Mapping[str, pd.DataFrame],
                 fig_dir: Path, geo: Path = DEFAULT_GEO) -> list[Path]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from shapely.geometry import shape

    fig_dir.mkdir(parents=True, exist_ok=True)
    written = []
    feats = json.loads(Path(geo).read_text())["features"]

    def outlines(ax):
        for f in feats:
            g = shape(f["geometry"])
            for poly in getattr(g, "geoms", [g]):
                x, y = poly.exterior.xy
                ax.plot(x, y, color="#8a8a85", lw=0.4)

    # Mapa de delta_B por celda.
    cd = cell_delta(frame).merge(cells[["ID", "lon", "lat"]], on="ID", how="left")
    lim = float(np.nanpercentile(np.abs(cd[["timesfm", "llr"]].to_numpy()), 98)) or 0.1
    fig, axes = plt.subplots(1, 2, figsize=(11, 7), sharex=True, sharey=True, constrained_layout=True)
    for ax, m, title in zip(axes, ("timesfm", "llr"), ("TimesFM", "LLR (Palacios)")):
        sc = ax.scatter(cd["lon"], cd["lat"], c=cd[m], s=2, cmap="RdBu", vmin=-lim, vmax=lim, linewidths=0)
        outlines(ax)
        ax.set_title(f"{title}: P_pred(B) − P_obs(B), B = [20, 24) °C", fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlabel("lon")
    axes[0].set_ylabel("lat")
    fig.colorbar(sc, ax=axes, shrink=0.6, label="Δ_B (proporción)")
    written.append(fig_dir / "mapa_delta_B.png")
    fig.savefig(written[-1], dpi=150)
    plt.close(fig)

    # Heatmap zona x anio de delta_B.
    za = tables["zona_anio"]
    if len(za):
        fig, axes = plt.subplots(1, 2, figsize=(11, 0.45 * za["zone_id"].nunique() + 2), constrained_layout=True)
        zones = list(dict.fromkeys(za["zone_id"]))
        years = sorted(za["anio"].unique())
        vals = {m: za[za.model == m].pivot(index="zone_id", columns="anio", values="delta_B").reindex(zones)[years]
                for m in ("timesfm", "llr")}
        lim = float(np.nanmax(np.abs(np.concatenate([v.to_numpy().ravel() for v in vals.values()])))) or 0.1
        labels = za.drop_duplicates("zone_id").set_index("zone_id")["zone_label"].reindex(zones)
        for ax, (m, v), title in zip(axes, vals.items(), ("TimesFM", "LLR (Palacios)")):
            im = ax.imshow(v.to_numpy(), cmap="RdBu", vmin=-lim, vmax=lim, aspect="auto")
            ax.set_xticks(range(len(years)), [str(y) for y in years])
            ax.set_yticks(range(len(zones)), [f"{z} {l}" for z, l in labels.items()], fontsize=7)
            for i in range(v.shape[0]):
                for j in range(v.shape[1]):
                    ax.text(j, i, f"{v.iat[i, j]:+.3f}", ha="center", va="center", fontsize=6,
                            color="white" if abs(v.iat[i, j]) > 0.6 * lim else "#1a1a19")
            ax.set_title(f"{title}: Δ_B por zona y año", fontsize=10)
        fig.colorbar(im, ax=axes, shrink=0.6, label="Δ_B (proporción)")
        written.append(fig_dir / "heatmap_zona_anio.png")
        fig.savefig(written[-1], dpi=150)
        plt.close(fig)

    # Densidades por anio en 15-28 C (bins de 0,1 C).
    width = 0.1
    edges = _edges(width)
    centers = edges[:-1] + width / 2
    rng = (centers >= FIG_RANGE[0]) & (centers <= FIG_RANGE[1])
    years = sorted(frame["year"].unique())
    fig, axes = plt.subplots(1, len(years), figsize=(3.2 * len(years), 3.4), sharey=True, constrained_layout=True)
    axes = np.atleast_1d(axes)
    yr = frame["year"].to_numpy()
    for ax, y in zip(axes, years):
        sel = yr == y
        for col, lab in (("obs", "obs"), ("timesfm", "TimesFM"), ("llr", "LLR"), ("clim", "clim")):
            v = frame[col].to_numpy()[sel]
            v = v[~np.isnan(v)]
            counts, _ = _hist(v, width)
            ax.plot(centers[rng], counts[rng] / max(len(v), 1) / width, color=COLORS[col], lw=1.5 if col == "obs" else 1.2,
                    ls="--" if col == "clim" else "-", label=lab)
        ax.axvspan(B_LO, B_HI, color="#f0efec", zorder=0)
        ax.axvspan(BP_LO, BP_HI, color="#fbe3d9", zorder=0)
        ax.set_title(str(y), fontsize=10)
        ax.set_xlabel("Td (°C)")
    axes[0].set_ylabel("densidad")
    axes[0].legend(fontsize=7, frameon=False)
    written.append(fig_dir / "densidad_anio.png")
    fig.savefig(written[-1], dpi=150)
    plt.close(fig)
    return written


# --------------------------------------------------------------------------- salida

def build_provenance(*, n_cells: int, outputs: Sequence[Path], bead_id: str, palacios: Path, tfm: Path,
                     n_boot: int, seed: int, limit_ids: int | None) -> prov.MetricProvenance:
    base = _kl_provenance(n_cells=n_cells, outputs=outputs, bead_id=bead_id, palacios=palacios, tfm=tfm)
    sample = f" Muestra de {limit_ids} celdas (semilla {seed}), no es el panel completo." if limit_ids else ""
    return replace(base, seeds=(seed,), notes=(
        f"Divergencia calida: delta = P_pred(B) - P_obs(B) para B = [{B_LO}, {B_HI}) y B' = [{BP_LO}, {BP_HI}] C, "
        f"share = n*delta / total nacional, contribucion de B a KL(obs || metodo) (bins de {BIN_COARSE} C, "
        f"Jeffreys {ALPHA}), sesgo condicional, por zona, banda DEM, departamento, tier, anio, mes, anio-mes y "
        f"zona x anio (zonas que suman {COVER:.0%} del deficit de TimesFM). Metodos: TimesFM tmin_anom_full, "
        f"Palacios pred_tuned (llr) y pred_clim (referencia), backtest limpio 2013-2016, mismo filtro que kl.py. "
        f"IC 95 % bootstrap de bloques ({BLOCK_DEG:g} grados y mes-anio, {n_boot} replicas, semilla {seed}) "
        f"para delta_B por zona y anio. Palacios leido de {palacios}, TimesFM de {tfm}.{sample} "
        f"Pesos de TimesFM de uso no comercial."))


def write_outputs(tables: Mapping[str, pd.DataFrame], hist: pd.DataFrame, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for name in CUTS:
        path = out_dir / f"{name}.csv"
        tables[name].to_csv(path, index=False, float_format="%.6g")
        written.append(path)
    path = out_dir / "hist_nacional.csv"
    hist.to_csv(path, index=False)
    written.append(path)
    return written


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--palacios", type=Path, default=DEFAULT_PALACIOS)
    parser.add_argument("--timesfm", type=Path, default=DEFAULT_TFM)
    parser.add_argument("--zone-table", type=Path, default=DEFAULT_ZONE)
    parser.add_argument("--support-distance", type=Path, default=DEFAULT_SUPPORT)
    parser.add_argument("--static", type=Path, default=DEFAULT_STATIC)
    parser.add_argument("--geo", type=Path, default=DEFAULT_GEO)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--n-boot", type=int, default=N_BOOT)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--limit-ids", type=int, default=None,
                        help="prueba rapida: solo N celdas sorteadas (no usar para resultados)")
    parser.add_argument("--no-figs", action="store_true")
    parser.add_argument("--bead-id", default="tdew-214.19")
    parser.add_argument("--registry-path", type=Path, default=prov.DEFAULT_REGISTRY_PATH)
    parser.add_argument("--repo-root", type=Path, default=prov.REPO_ROOT)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    for target in (args.out_dir, args.registry_path):
        refuse_under_res(target)

    t0 = time.time()
    ids = sample_ids(args.palacios, args.limit_ids, args.seed) if args.limit_ids else None
    frame = load_pairs(args.palacios, args.timesfm, ids)
    uniq = np.unique(frame["ID"].to_numpy())
    logger.info("%d pares, %d celdas (%.0f s)", len(frame), len(uniq), time.time() - t0)
    cells = cell_table(uniq, args.zone_table, args.support_distance, args.static, args.geo)
    tables = compute(frame, cells, n_boot=args.n_boot, seed=args.seed)
    hist = national_hist(frame)
    written = write_outputs(tables, hist, args.out_dir)
    record = build_provenance(n_cells=len(uniq), outputs=written, bead_id=args.bead_id, palacios=args.palacios,
                              tfm=args.timesfm, n_boot=args.n_boot, seed=args.seed, limit_ids=args.limit_ids)
    prov.record_metric_provenance(record, registry_path=args.registry_path, repo_root=args.repo_root)
    if not args.no_figs:
        make_figures(frame, cells, tables, args.out_dir / "figs", args.geo)
    cols = ["model", "n", "delta_B", "share_B", "delta_Bp", "kl_B", "bias_obs_B", "bias_pred_Bp"]
    for cut, keys in (("anio", ["anio"]), ("zona", ["zone_id", "zone_label"])):
        print(f"--- {cut} ---")
        print(tables[cut][keys + cols].sort_values("share_B", ascending=False).head(24).round(4).to_string(index=False))
    logger.info("listo en %.0f s", time.time() - t0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
