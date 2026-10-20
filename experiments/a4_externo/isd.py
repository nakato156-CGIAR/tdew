"""Lectura de NOAA NCEI ISD global-hourly (CSV) y agregacion a Td media diaria.

Formato del campo ``DEW`` (y ``TMP``): ``"+0185,1"`` = valor en decimas de grado C con
signo, coma, codigo de calidad. ``+9999`` es dato faltante.

Control de calidad aplicado a cada observacion:

- se descarta ``+9999``;
- se aceptan solo los codigos de calidad 0, 1, 4, 5 y 9 (pasaron chequeos de limites o
  todos los chequeos); se rechazan 2, 3, 6, 7 (sospechoso/erroneo) y los codigos de
  dato editado o estimado (A, C, I, M, P, R, U);
- se descarta Td fuera de [-40, 35] °C;
- se descarta Td > T + 0,5 °C cuando la temperatura del mismo registro es valida
  (sobresaturacion fisicamente implausible).

Agregacion diaria (dia local, UTC-5, sin horario de verano en el Peru):

1. las observaciones de una misma hora (p. ej. SYNOP FM-12 y METAR FM-15 a la misma
   hora) se resumen con la mediana, de modo que cada hora pesa una vez;
2. el dia se divide en cuatro bloques de 6 h (00-06, 06-12, 12-18, 18-24 locales);
3. un dia es valido si tiene al menos ``min_hours`` horas validas (4 por defecto) y al
   menos una hora en cada uno de los cuatro bloques;
4. Td diaria = promedio de las cuatro medias de bloque (evita que un muestreo diurno
   denso domine la media).

Las estaciones que solo reportan de dia quedan fuera por el punto 3; se informa cuantas.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ACCEPTED_QC = frozenset("01459")
MISSING = 9999
TD_RANGE = (-40.0, 35.0)
SUPERSAT_TOL = 0.5
LOCAL_OFFSET_H = -5
N_BLOCKS = 4


def parse_value(series: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """``"+0185,1"`` -> (18.5, "1"). Faltantes y no parseables -> NaN, ""."""
    s = series.fillna("").astype(str)
    parts = s.str.split(",", n=1, expand=True)
    if parts.shape[1] < 2:
        parts[1] = ""
    raw = pd.to_numeric(parts[0], errors="coerce")
    qc = parts[1].fillna("").str.strip().to_numpy(dtype=object)
    value = raw.to_numpy(dtype=float)
    value = np.where(np.abs(value) == MISSING, np.nan, value / 10.0)
    return value, qc


def clean_hourly(frame: pd.DataFrame) -> pd.DataFrame:
    """Filas validas de Td con su hora local. Entra el CSV de ISD con DATE, DEW, TMP."""
    td, td_qc = parse_value(frame["DEW"])
    if "TMP" in frame:
        t, t_qc = parse_value(frame["TMP"])
        t_ok = np.isin(t_qc, list(ACCEPTED_QC)) & np.isfinite(t)
        t = np.where(t_ok, t, np.nan)
    else:
        t = np.full(len(frame), np.nan)
    ok = np.isfinite(td) & np.isin(td_qc, list(ACCEPTED_QC))
    ok &= (td >= TD_RANGE[0]) & (td <= TD_RANGE[1])
    ok &= ~(np.isfinite(t) & (td > t + SUPERSAT_TOL))
    utc = pd.to_datetime(frame["DATE"], errors="coerce")
    ok &= utc.notna().to_numpy()
    local = utc[ok] + pd.Timedelta(hours=LOCAL_OFFSET_H)
    return pd.DataFrame({"local": local.dt.floor("h").to_numpy(), "td": td[ok]})


def daily_from_hourly(hourly: pd.DataFrame, *, min_hours: int = 4, min_blocks: int = N_BLOCKS) -> pd.DataFrame:
    """Td media diaria con el criterio de completitud del modulo.

    ``min_blocks < 4`` es la variante de sensibilidad (admite estaciones sin
    observaciones nocturnas); la media diaria es entonces la de los bloques presentes.

    Devuelve FECHA, TD, n_hours, n_blocks solo para los dias validos.
    """
    cols = ["FECHA", "TD", "n_hours", "n_blocks"]
    if hourly.empty:
        return pd.DataFrame(columns=cols)
    per_hour = hourly.groupby("local", as_index=False)["td"].median()
    per_hour["FECHA"] = per_hour["local"].dt.normalize()
    per_hour["block"] = per_hour["local"].dt.hour // (24 // N_BLOCKS)
    blocks = per_hour.groupby(["FECHA", "block"])["td"].agg(["mean", "size"]).reset_index()
    day = blocks.groupby("FECHA").agg(TD=("mean", "mean"), n_hours=("size", "sum"),
                                     n_blocks=("block", "nunique")).reset_index()
    day = day[(day["n_hours"] >= min_hours) & (day["n_blocks"] >= min_blocks)]
    return day[cols].reset_index(drop=True)


def read_isd_csv(path: Path | str) -> pd.DataFrame:
    """CSV global-hourly con las columnas necesarias, todo como texto."""
    return pd.read_csv(path, usecols=lambda c: c in {"STATION", "DATE", "DEW", "TMP", "REPORT_TYPE"},
                       dtype=str, low_memory=False)


def station_daily(files: list[Path], *, min_hours: int = 4, min_blocks: int = N_BLOCKS) -> tuple[pd.DataFrame, dict]:
    """Une los CSV anuales de una estacion y agrega a diario. Devuelve (diario, conteos)."""
    frames = [read_isd_csv(f) for f in files]
    frames = [f for f in frames if not f.empty]
    raw = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["DATE", "DEW", "TMP"])
    n_raw = len(raw)
    n_dew = int((~raw["DEW"].fillna("+9999,9").str.startswith("+9999")).sum()) if n_raw else 0
    hourly = clean_hourly(raw) if n_raw else pd.DataFrame(columns=["local", "td"])
    daily = daily_from_hourly(hourly, min_hours=min_hours, min_blocks=min_blocks)
    counts = {"n_records": n_raw, "n_dew_reported": n_dew, "n_dew_valid": len(hourly),
              "n_days_valid": len(daily)}
    return daily, counts
