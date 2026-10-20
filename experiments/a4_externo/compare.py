"""Contraste por estacion: Td de estaciones ISD frente a PISCO, a los dos productos 2017-2020
y a ERA5/ERA5-Land (Open-Meteo), en Td y en anomalias.

Fuentes por estacion (celda PISCO que contiene la estacion, mapeo de ``grid``):

- ``pisco``: TD de ``$RES/bucketed_training_data`` (PISCO v1.1), 2009-2016;
- ``palacios``: ``TD_predicted`` de ``$RES/tuning/predictions_2017_2020`` (``tuned``);
- ``timesfm``: ``pred`` de ``$WORK/preds_real`` (``tmin_anom_full``), 2017-2020;
- ``era5`` y ``era5_land``: Td media diaria en la coordenada de la estacion, 2009-2020.

Anomalias: cada serie menos su climatologia armonica (media + 3 armonicos anuales)
ajustada en 2009-2016. La estacion usa la suya; PISCO, ``palacios`` y ``timesfm`` usan la
de PISCO en la celda (los productos continuan a PISCO); ERA5 y ERA5-Land la propia.
Asi la anomalia no depende del desfase fijo estacion-celda (elevacion, ubicacion).

Errores: ``fuente - estacion``. Las metricas "comunes" usan solo dias en que todas las
fuentes del periodo tienen dato.

Uso::

    uv run python -m experiments.a4_externo.compare --work /home/cvelasquez/tdew_timesfm/a4
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

from experiments.timesfm import paths

from . import grid, isd, openmeteo

logger = logging.getLogger("a4.compare")
OUT = Path("reports/paper_nuevo/resultados")
CLIM_YEARS = (2009, 2016)
N_HARM = 3
MIN_CLIM_DAYS = 730
MIN_CLIM_DAYS_PER_MONTH = 30
MIN_STATION_DAYS = 180
# muestra -> (fuentes 2009-2016, fuentes 2017-2020)
SAMPLES = {
    "productos": (("pisco",), ("palacios", "timesfm")),
    "con_reanalisis": (("pisco", "era5", "era5_land"), ("palacios", "timesfm", "era5", "era5_land")),
}


# ---------------------------------------------------------------------- estaciones

def build_station_daily(work: Path, stations: pd.DataFrame, min_hours: int = 4,
                        min_blocks: int = isd.N_BLOCKS) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = work / "isd_raw"
    frames, counts = [], []
    for st in stations["station"]:
        files = sorted(raw.glob(f"*/{st}.csv"))
        daily, c = isd.station_daily(files, min_hours=min_hours, min_blocks=min_blocks)
        daily["station"] = st
        frames.append(daily)
        c["station"] = st
        c["n_files"] = len(files)
        counts.append(c)
        logger.info("%s: %s", st, c)
    return pd.concat(frames, ignore_index=True), pd.DataFrame(counts)


# ---------------------------------------------------------------------- climatologia

def _design(doy: np.ndarray) -> np.ndarray:
    w = 2 * np.pi * np.asarray(doy, dtype=float) / 365.25
    cols = [np.ones_like(w)]
    for k in range(1, N_HARM + 1):
        cols += [np.cos(k * w), np.sin(k * w)]
    return np.column_stack(cols)


def harmonic_clim(dates: pd.Series, values: pd.Series) -> np.ndarray | None:
    """Coeficientes de la climatologia armonica en 2009-2016, o None si no alcanza."""
    d = pd.to_datetime(dates)
    m = d.dt.year.between(*CLIM_YEARS) & values.notna()
    if m.sum() < MIN_CLIM_DAYS:
        return None
    per_month = d[m].dt.month.value_counts()
    if len(per_month) < 12 or per_month.min() < MIN_CLIM_DAYS_PER_MONTH:
        return None
    coef, *_ = np.linalg.lstsq(_design(d[m].dt.dayofyear), values[m].to_numpy(float), rcond=None)
    return coef


def clim_value(coef: np.ndarray, dates: pd.Series) -> np.ndarray:
    return _design(pd.to_datetime(dates).dt.dayofyear) @ coef


# ---------------------------------------------------------------------- metricas

def metrics(err: np.ndarray, pred: np.ndarray, obs: np.ndarray) -> dict:
    n = len(err)
    if n < 3:
        return {"n_dias": n, "sesgo": np.nan, "rmse": np.nan, "mae": np.nan, "r": np.nan}
    r = np.corrcoef(pred, obs)[0, 1] if np.std(pred) > 0 and np.std(obs) > 0 else np.nan
    return {"n_dias": n, "sesgo": float(err.mean()), "rmse": float(np.sqrt((err ** 2).mean())),
            "mae": float(np.abs(err).mean()), "r": float(r)}


def score(long: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """``long`` trae fuente, station, FECHA, kind (td/anom), pred, obs."""
    rows = []
    for k, g in long.groupby(keys):
        k = k if isinstance(k, tuple) else (k,)
        row = dict(zip(keys, k))
        row.update(metrics((g["pred"] - g["obs"]).to_numpy(), g["pred"].to_numpy(), g["obs"].to_numpy()))
        row["n_estaciones"] = g["station"].nunique()
        rows.append(row)
    return pd.DataFrame(rows)


def station_mean(per_station: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
    """Mediana y media entre estaciones de las metricas por estacion."""
    agg = per_station.groupby(keys).agg(
        n_estaciones=("station", "nunique"), rmse_mediana=("rmse", "median"), rmse_media=("rmse", "mean"),
        sesgo_mediana=("sesgo", "median"), r_mediana=("r", "median"), n_dias=("n_dias", "sum"))
    return agg.reset_index()


def paired_bootstrap(long: pd.DataFrame, a: str, b: str, *, reps: int = 2000, seed: int = 0) -> dict:
    """RMSE(a) - RMSE(b) agrupado sobre los mismos dias, IC 95 % remuestreando estaciones."""
    wide = long.pivot_table(index=["station", "FECHA"], columns="fuente", values="err").dropna(subset=[a, b])
    if wide.empty:
        return {}
    per = wide.groupby(level="station").agg(sa=(a, lambda x: (x ** 2).sum()), sb=(b, lambda x: (x ** 2).sum()),
                                            n=(a, "size"))
    point = np.sqrt(per["sa"].sum() / per["n"].sum()) - np.sqrt(per["sb"].sum() / per["n"].sum())
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(per), size=(reps, len(per)))
    sa, sb, n = (per[c].to_numpy()[idx].sum(axis=1) for c in ("sa", "sb", "n"))
    boot = np.sqrt(sa / n) - np.sqrt(sb / n)
    return {"a": a, "b": b, "delta_rmse": float(point), "ic95_lo": float(np.quantile(boot, 0.025)),
            "ic95_hi": float(np.quantile(boot, 0.975)), "n_estaciones": len(per), "n_dias": int(per["n"].sum())}


# ---------------------------------------------------------------------- indices

def oni_annual(path: Path) -> pd.DataFrame:
    oni = pd.read_csv(path, sep=r"\s+")
    oni = oni[oni["YR"].between(2009, 2020)]
    return oni.groupby("YR").agg(oni_media=("ANOM", "mean"), oni_max=("ANOM", "max"),
                                 oni_min=("ANOM", "min")).reset_index().rename(columns={"YR": "anio"})


def nino12_annual(path: Path) -> pd.DataFrame:
    sst = pd.read_csv(path, sep=r"\s+")
    sst.columns = ["YR", "MON", "N12", "N12A", "N3", "N3A", "N4", "N4A", "N34", "N34A"]
    sst = sst[sst["YR"].between(2009, 2020)]
    return sst.groupby("YR").agg(nino12_media=("N12A", "mean"), nino12_max=("N12A", "max")).reset_index() \
        .rename(columns={"YR": "anio"})


# ---------------------------------------------------------------------- principal

def load_grid(cells: np.ndarray) -> dict[str, pd.DataFrame]:
    res = paths.RES
    pisco = grid.read_cells(res / "bucketed_training_data", [f"train_{y}.parquet" for y in range(2009, 2017)],
                            cells, ["ID", "FECHA", "TD", "TMIN"])
    pal = grid.read_cells(res / "tuning/predictions_2017_2020", ["pred.parquet"], cells,
                          ["ID", "FECHA", "TD_predicted"]).rename(columns={"TD_predicted": "TD"})
    tfm = grid.read_cells(paths.WORK / "preds_real", ["pred.parquet"], cells, ["ID", "day", "pred"])
    tfm["FECHA"] = pd.Timestamp("2017-01-01") + pd.to_timedelta(tfm["day"].astype(int), unit="D")
    tfm = tfm.rename(columns={"pred": "TD"})[["ID", "FECHA", "TD"]]
    out = {"pisco": pisco[["ID", "FECHA", "TD"]], "palacios": pal, "timesfm": tfm}
    for k, v in out.items():
        v["FECHA"] = pd.to_datetime(v["FECHA"]).dt.normalize()
        v["TD"] = v["TD"].astype(float)
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--min-hours", type=int, default=4)
    parser.add_argument("--min-blocks", type=int, default=isd.N_BLOCKS,
                        help="4 = criterio principal; <4 = sensibilidad, sufijo _h<h>b<b> en las salidas")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    work, out = args.work, args.out
    out.mkdir(parents=True, exist_ok=True)

    stations = pd.read_csv(work / "isd_meta/stations_pe.csv", dtype={"station": str, "USAF": str, "WBAN": str})
    tag = f"h{args.min_hours}" + ("" if args.min_blocks == isd.N_BLOCKS else f"b{args.min_blocks}")
    suffix = "" if (args.min_hours, args.min_blocks) == (4, isd.N_BLOCKS) else f"_{tag}"
    daily_path = work / f"stations_daily_{tag}.parquet"
    if daily_path.exists():
        daily = pd.read_parquet(daily_path)
        counts = pd.read_csv(work / f"stations_counts_{tag}.csv", dtype={"station": str})
    else:
        daily, counts = build_station_daily(work, stations, args.min_hours, args.min_blocks)
        daily.to_parquet(daily_path, index=False)
        counts.to_csv(work / f"stations_counts_{tag}.csv", index=False)
    daily["FECHA"] = pd.to_datetime(daily["FECHA"])
    daily["anio"] = daily["FECHA"].dt.year

    stations["ID"] = grid.lonlat_to_id(stations["LON"], stations["LAT"])
    stations = stations[stations["ID"] >= 0]
    cell_lon, cell_lat = grid.id_to_lonlat(stations["ID"])
    stations["cell_lon"], stations["cell_lat"] = cell_lon, cell_lat
    (work / "openmeteo_raw").mkdir(parents=True, exist_ok=True)
    stations["elev_celda_dem"] = openmeteo.elevations(cell_lat, cell_lon, work / "openmeteo_raw" / "elev_celdas.json")
    stations["dif_elev_est_menos_celda"] = stations["ELEV(M)"] - stations["elev_celda_dem"]

    # dias validos por estacion y periodo
    per_year = daily.pivot_table(index="station", columns="anio", values="TD", aggfunc="size").fillna(0)
    stations = stations.merge(counts, on="station", how="left")
    stations["dias_2009_2016"] = stations["station"].map(per_year.loc[:, [c for c in per_year if c <= 2016]].sum(axis=1)).fillna(0)
    stations["dias_2017_2020"] = stations["station"].map(per_year.loc[:, [c for c in per_year if c >= 2017]].sum(axis=1)).fillna(0)
    used = stations[(stations["dias_2009_2016"] + stations["dias_2017_2020"]) > 0].copy()

    # las respuestas JSON quedan en cache por estacion y modelo en openmeteo_raw/
    era, era_elev = openmeteo.fetch_stations(used, work)
    era.to_parquet(work / f"era5_points{suffix}.parquet", index=False)
    era["FECHA"] = pd.to_datetime(era["FECHA"])
    for model in openmeteo.MODELS:
        e = era_elev[era_elev["model"] == model].set_index("station")["elev_modelo"]
        used[f"elev_{model}"] = used["station"].map(e)
    shift = era_elev[era_elev["model"] == "era5_land"].set_index("station")["desplazamiento_este_grados"]
    used["era5_land_desplazamiento_este"] = used["station"].map(shift)

    gridded = load_grid(used["ID"].unique())
    cell_of = used.set_index("station")["ID"]

    # ---------------- tabla larga: fuente, station, FECHA, pred, obs, anomalias
    rows = []
    clim_rows = []
    for st in used["station"]:
        obs = daily[daily["station"] == st][["FECHA", "TD"]].rename(columns={"TD": "obs"})
        coef_obs = harmonic_clim(obs["FECHA"], obs["obs"])
        cell = cell_of[st]
        pis = gridded["pisco"][gridded["pisco"]["ID"] == cell][["FECHA", "TD"]]
        coef_pis = harmonic_clim(pis["FECHA"], pis["TD"])
        series = {"pisco": pis, "palacios": gridded["palacios"][gridded["palacios"]["ID"] == cell][["FECHA", "TD"]],
                  "timesfm": gridded["timesfm"][gridded["timesfm"]["ID"] == cell][["FECHA", "TD"]]}
        coefs = {"pisco": coef_pis, "palacios": coef_pis, "timesfm": coef_pis}
        for model in openmeteo.MODELS:
            e = era[(era["station"] == st) & (era["model"] == model)][["FECHA", "TD"]]
            series[model] = e
            coefs[model] = harmonic_clim(e["FECHA"], e["TD"])
        clim_rows.append({"station": st, "clim_estacion": coef_obs is not None,
                          **{f"clim_{k}": coefs[k] is not None for k in ("pisco", "era5", "era5_land")}})
        for name, s in series.items():
            m = obs.merge(s.dropna(subset=["TD"]), on="FECHA").rename(columns={"TD": "pred"})
            if m.empty:
                continue
            m["fuente"], m["station"] = name, st
            if coef_obs is not None and coefs[name] is not None:
                m["obs_anom"] = m["obs"] - clim_value(coef_obs, m["FECHA"])
                m["pred_anom"] = m["pred"] - clim_value(coefs[name], m["FECHA"])
            else:
                m["obs_anom"] = np.nan
                m["pred_anom"] = np.nan
            rows.append(m)
    pairs = pd.concat(rows, ignore_index=True)
    pairs["anio"] = pairs["FECHA"].dt.year
    pairs["periodo"] = np.where(pairs["anio"] <= 2016, "2009-2016", "2017-2020")
    pairs.to_parquet(work / f"pares_estacion_fuente{suffix}.parquet", index=False)

    td = pairs.assign(kind="td")[["fuente", "station", "FECHA", "anio", "periodo", "kind", "pred", "obs"]]
    an = pairs.dropna(subset=["obs_anom", "pred_anom"]).assign(kind="anom")
    an = an[["fuente", "station", "FECHA", "anio", "periodo", "kind", "pred_anom", "obs_anom"]] \
        .rename(columns={"pred_anom": "pred", "obs_anom": "obs"})
    long = pd.concat([td, an], ignore_index=True)

    # muestras comunes por periodo: dias con todas las fuentes del periodo y estaciones con
    # al menos MIN_STATION_DAYS dias comunes en el periodo
    def common(frame, sources):
        f = frame[frame["fuente"].isin(sources)]
        k = f.groupby(["kind", "station", "FECHA"])["fuente"].transform("nunique")
        f = f[k == len(sources)]
        days = f.groupby(["kind", "station"])["FECHA"].transform("nunique")
        return f[days >= MIN_STATION_DAYS]

    tables = {}
    comm_by_sample = {}
    for sample, (past_src, fut_src) in SAMPLES.items():
        past = common(long[long["periodo"] == "2009-2016"], past_src)
        fut = common(long[long["periodo"] == "2017-2020"], fut_src)
        c = pd.concat([past, fut], ignore_index=True)
        c["err"] = c["pred"] - c["obs"]
        c["muestra"] = sample
        comm_by_sample[sample] = c
    comm = pd.concat(comm_by_sample.values(), ignore_index=True)

    tables["a4_por_anio"] = score(comm, ["muestra", "kind", "fuente", "anio"])
    tables["a4_por_periodo"] = score(comm, ["muestra", "kind", "fuente", "periodo"])
    tables["a4_todas_las_parejas_por_periodo"] = score(long, ["kind", "fuente", "periodo"])
    per_station = score(comm, ["muestra", "kind", "fuente", "periodo", "station"])
    tables["a4_por_estacion"] = per_station
    tables["a4_resumen_entre_estaciones"] = station_mean(per_station, ["muestra", "kind", "fuente", "periodo"])
    tables["a4_por_estacion_anio_anom"] = score(comm[(comm["kind"] == "anom")],
                                                ["muestra", "fuente", "station", "anio"])

    boots = []
    pairs_fut = [("timesfm", "palacios"), ("era5_land", "palacios"), ("era5_land", "timesfm"), ("era5", "palacios")]
    pairs_past = [("era5_land", "pisco"), ("era5", "pisco")]
    for sample, c in comm_by_sample.items():
        for kind in ("td", "anom"):
            for periodo, plist in (("2017-2020", pairs_fut), ("2009-2016", pairs_past)):
                f = c[(c["kind"] == kind) & (c["periodo"] == periodo)]
                for a, b in plist:
                    if a in set(f["fuente"]) and b in set(f["fuente"]):
                        r = paired_bootstrap(f, a, b)
                        if r:
                            boots.append({"muestra": sample, "kind": kind, "periodo": periodo, **r})
    tables["a4_delta_rmse_bootstrap"] = pd.DataFrame(boots)

    # robustez: RMSE agrupado dejando fuera una estacion a la vez
    loso = []
    for st in sorted(comm["station"].unique()):
        sub = comm[comm["station"] != st]
        t = score(sub, ["muestra", "kind", "fuente", "periodo"])
        t.insert(0, "estacion_excluida", st)
        loso.append(t)
    tables["a4_dejar_una_estacion_fuera"] = pd.concat(loso, ignore_index=True)

    # ---------------- desacuerdo entre productos por año en las celdas de estacion, con ONI y Niño 1+2
    pal = gridded["palacios"].merge(gridded["timesfm"], on=["ID", "FECHA"], suffixes=("_pal", "_tfm"))
    pal["anio"] = pal["FECHA"].dt.year
    pal["d"] = pal["TD_tfm"] - pal["TD_pal"]
    dis = pal.groupby("anio").agg(n=("d", "size"), sesgo_tfm_menos_pal=("d", "mean"),
                                  rmse_entre_productos=("d", lambda x: float(np.sqrt((x ** 2).mean())))).reset_index()
    nat = pd.read_csv("reports/timesfm_benchmark/real_limpio/agreement_by_year_limpio.csv") \
        .rename(columns={"year": "anio", "rmse": "rmse_entre_productos_nacional", "bias": "sesgo_nacional"})
    dis = dis.merge(nat[["anio", "rmse_entre_productos_nacional", "sesgo_nacional"]], on="anio", how="left")
    err = tables["a4_por_anio"]
    err = err[err["muestra"] == "productos"]
    for kind in ("td", "anom"):
        for src in ("palacios", "timesfm"):
            e = err[(err["kind"] == kind) & (err["fuente"] == src)].set_index("anio")["rmse"]
            dis[f"rmse_{kind}_{src}_vs_estacion"] = dis["anio"].map(e)
    idx = oni_annual(work / "isd_meta/oni.ascii.txt").merge(nino12_annual(work / "indices/sstoi.indices"), on="anio")
    tables["a4_desacuerdo_oni"] = dis.merge(idx, on="anio", how="left")
    tables["a4_indices_2009_2020"] = idx

    clim = pd.DataFrame(clim_rows)
    st_table = used.merge(clim, on="station", how="left")
    keep = ["station", "USAF", "STATION NAME", "ICAO", "LAT", "LON", "ELEV(M)", "ID", "cell_lon", "cell_lat",
            "elev_celda_dem", "dif_elev_est_menos_celda", "elev_era5", "elev_era5_land", "era5_land_desplazamiento_este", "n_records",
            "n_dew_reported", "n_dew_valid", "n_days_valid", "dias_2009_2016", "dias_2017_2020",
            "clim_estacion", "clim_pisco", "clim_era5", "clim_era5_land"]
    st_table = st_table[[c for c in keep if c in st_table]]
    used_comm = comm[comm["muestra"] == "productos"].groupby("station")["periodo"].unique().map(lambda v: ",".join(sorted(v)))
    st_table["en_muestra_productos"] = st_table["station"].map(used_comm).fillna("")
    used_r = comm[comm["muestra"] == "con_reanalisis"].groupby("station")["periodo"].unique().map(
        lambda v: ",".join(sorted(v)))
    st_table["en_muestra_con_reanalisis"] = st_table["station"].map(used_r).fillna("")
    tables["a4_estaciones"] = st_table
    excl = stations[~stations["station"].isin(used["station"])][["station", "STATION NAME", "LAT", "LON", "n_records",
                                                                  "n_dew_reported", "n_dew_valid", "n_days_valid"]]
    tables["a4_estaciones_excluidas"] = excl
    tables["a4_dias_por_estacion_anio"] = per_year.astype(int).reset_index()

    for name, t in tables.items():
        t.to_csv(out / f"{name}{suffix}.csv", index=False, float_format="%.4f")
        logger.info("%s\n%s", name, t.head(60).to_string())
    meta = {"min_hours": args.min_hours, "min_blocks": args.min_blocks, "clim_years": CLIM_YEARS, "n_harm": N_HARM,
            "min_clim_days": MIN_CLIM_DAYS, "min_station_days": MIN_STATION_DAYS, "samples": SAMPLES,
            "res": str(paths.RES), "work_timesfm": str(paths.WORK)}
    (out / f"a4_config{suffix}.json").write_text(json.dumps(meta, indent=2, default=list))
    metric_files = [str(out / f"{name}{suffix}.csv") for name in METRIC_TABLES]
    write_provenance(metric_files, tag=tag, n_cells=int(comm["station"].map(cell_of).nunique()),
                     n_stations=int(comm["station"].nunique()), station_file=str(out / f"a4_estaciones{suffix}.csv"),
                     meta=meta)
    return 0


# tablas con metricas de error frente a estacion; las demas son auxiliares (lista de
# estaciones, conteos de dias, indices ENSO) y se excluyen en tests/test_metric_provenance.py
METRIC_TABLES = (
    "a4_por_anio", "a4_por_periodo", "a4_todas_las_parejas_por_periodo", "a4_por_estacion",
    "a4_resumen_entre_estaciones", "a4_por_estacion_anio_anom", "a4_delta_rmse_bootstrap",
    "a4_dejar_una_estacion_fuera", "a4_desacuerdo_oni",
)


def write_provenance(output_files: list[str], *, tag: str, n_cells: int, n_stations: int,
                     station_file: str, meta: dict) -> None:
    from tdew_estimation import provenance as prov

    notes = (f"A4: error de Td y de anomalias de Td frente a estaciones ISD (NOAA NCEI global-hourly) "
             f"del Peru; criterio diario {tag}; {n_stations} estaciones en {n_cells} celdas PISCO. "
             "Fuentes: pisco (bucketed_training_data, 2009-2016), palacios (tuning/predictions_2017_2020, "
             "entrenado en 1981-2016, autorregresivo), timesfm (preds_real tmin_anom_full, zero-shot con "
             "contexto 1981-2016), era5 y era5_land (Open-Meteo, puntos). La columna kind distingue td y "
             "anom; anomalias respecto de climatologia armonica 2009-2016 de cada fuente. Bootstrap de "
             f"estaciones 2000 replicas semilla 0. Configuracion: {json.dumps(meta, default=list)}")
    record = prov.MetricProvenance(
        run_id=prov.new_run_id(), generated_at=prov.now_iso(), git_commit=prov.git_commit(),
        bead_id="tdew-ra6", manifest_ref="docs/protocol/timesfm_manifest_addendum_real_2017_2020.yaml",
        model_family="comparison", model_id="multi", variant_label=f"a4_contraste_externo_{tag}",
        trained=True, training_period=("1981-01-01", "2016-12-31"), validation_period=None,
        test_period=("2009-01-01", "2020-12-31"), split_id="real_2017_2020+pisco_2009_2016",
        autoregressive=True, target_type="td_raw", climatology_used=True,
        climatology_role="anomaly_reference",
        inputs=("isd_global_hourly", "pisco", "palacios", "timesfm", "era5", "era5_land"),
        panel_id=f"isd_pe_estaciones_{tag}", panel_cell_count=n_cells, panel_file=station_file,
        output_files=tuple(output_files), seeds=(0,), notes=notes,
    )
    prov.record_metric_provenance(record)


if __name__ == "__main__":
    raise SystemExit(main())
