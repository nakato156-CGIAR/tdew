"""Td diaria de ERA5 (0,25°) y ERA5-Land (0,1°) en puntos, via la API publica de Open-Meteo.

No hay credenciales de CDS ni de Earth Engine en la estacion de trabajo. La API historica
de Open-Meteo (``archive-api.open-meteo.com``) sirve ERA5 y ERA5-Land sin clave para uso
no comercial (datos CC BY 4.0; ERA5 bajo la licencia de Copernicus). Parametros usados:

- ``daily=dew_point_2m_mean`` con ``timezone=America/Lima``: media diaria de las 24 horas
  del dia local (UTC-5), el mismo dia que se usa para las estaciones;
- ``elevation=nan``: desactiva la correccion por elevacion de Open-Meteo, de modo que el
  valor es el de la celda del reanalisis; ``cell_selection``: celda mas cercana en ERA5 y
  celda de tierra mas cercana en ERA5-Land.

Tambien se consulta la elevacion (DEM Copernicus 90 m de Open-Meteo) en el centro de la
celda PISCO de cada estacion, como aproximacion de la elevacion de la celda de 1 km.

Las respuestas JSON se guardan tal cual en ``<out>/openmeteo_raw/`` (datos no confiables,
solo se leen con ``json``).
"""

from __future__ import annotations

import json
import logging
import time
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
ELEVATION_URL = "https://api.open-meteo.com/v1/elevation"
MODELS = ("era5", "era5_land")
# ERA5-Land no tiene valores sobre el mar: en aeropuertos costeros la celda mas cercana
# puede ser oceanica (Trujillo, Pisco), asi que se pide la celda de tierra mas cercana.
CELL_SELECTION = {"era5": "nearest", "era5_land": "land"}
# si aun asi no hay dato, se desplaza el punto hacia el este en pasos de 0,1° (hasta 0,3°)
INLAND_STEP, INLAND_MAX_SHIFT = 0.1, 0.3
logger = logging.getLogger("a4.openmeteo")


def _fetch_json(url: str, dest: Path, *, retries: int = 4) -> dict:
    if dest.exists() and dest.stat().st_size > 0:
        return json.loads(dest.read_text())
    last = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                body = resp.read()
            data = json.loads(body)
            if data.get("error"):
                raise RuntimeError(data.get("reason"))
            dest.write_bytes(body)
            return data
        except Exception as exc:  # red inestable o limite de la API
            last = exc
            logger.warning("%s: %s (intento %d)", url[:120], exc, attempt + 1)
            time.sleep(30 * (attempt + 1))
    raise RuntimeError(f"fallo {url}: {last}")


def point_series(lat: float, lon: float, model: str, start: str, end: str, dest: Path) -> tuple[pd.DataFrame, float]:
    """(FECHA, TD) diaria y elevacion de la celda del modelo."""
    query = urllib.parse.urlencode({
        "latitude": f"{lat:.4f}", "longitude": f"{lon:.4f}", "start_date": start, "end_date": end,
        "daily": "dew_point_2m_mean", "models": model, "timezone": "America/Lima",
        "elevation": "nan", "cell_selection": CELL_SELECTION[model],
    })
    data = _fetch_json(f"{ARCHIVE_URL}?{query}", dest)
    daily = data["daily"]
    frame = pd.DataFrame({"FECHA": pd.to_datetime(daily["time"]),
                          "TD": pd.to_numeric(pd.Series(daily["dew_point_2m_mean"]), errors="coerce")})
    return frame, float(data.get("elevation", float("nan")))


def elevations(lats, lons, dest: Path) -> list[float]:
    """Elevacion DEM en lotes de 100 puntos."""
    out: list[float] = []
    lats, lons = list(lats), list(lons)
    for i in range(0, len(lats), 100):
        query = urllib.parse.urlencode({
            "latitude": ",".join(f"{v:.4f}" for v in lats[i:i + 100]),
            "longitude": ",".join(f"{v:.4f}" for v in lons[i:i + 100]),
        })
        data = _fetch_json(f"{ELEVATION_URL}?{query}", dest.with_name(f"{dest.stem}_{i}.json"))
        out.extend(float(v) for v in data["elevation"])
    return out


def fetch_stations(stations: pd.DataFrame, out: Path, start: str = "2009-01-01",
                   end: str = "2020-12-31") -> tuple[pd.DataFrame, pd.DataFrame]:
    """Series ERA5/ERA5-Land en las coordenadas de cada estacion.

    Devuelve (largo con station, model, FECHA, TD; tabla station, model, elev_modelo).
    """
    raw = out / "openmeteo_raw"
    raw.mkdir(parents=True, exist_ok=True)
    frames, elev = [], []
    for st in stations.itertuples():
        for model in MODELS:
            frame, z = point_series(st.LAT, st.LON, model, start, end,
                                    raw / f"{st.station}_{model}_{CELL_SELECTION[model]}.json")
            shift = 0.0
            # aeropuertos costeros sin celda ERA5-Land: se desplaza el punto tierra adentro (al este)
            while model == "era5_land" and frame["TD"].isna().all() and shift < INLAND_MAX_SHIFT:
                shift = round(shift + INLAND_STEP, 2)
                frame, z = point_series(st.LAT, st.LON + shift, model, start, end,
                                        raw / f"{st.station}_{model}_{CELL_SELECTION[model]}_este{shift:.2f}.json")
                time.sleep(1.0)
            frame["station"] = st.station
            frame["model"] = model
            frames.append(frame)
            elev.append({"station": st.station, "model": model, "elev_modelo": z, "desplazamiento_este_grados": shift})
            time.sleep(1.0)
    return pd.concat(frames, ignore_index=True), pd.DataFrame(elev)
