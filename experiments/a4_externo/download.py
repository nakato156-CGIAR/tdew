"""Descarga de estaciones ISD del Peru (global-hourly) y del indice ONI.

Fuente ISD: ``https://www.ncei.noaa.gov/data/global-hourly/access/<año>/<USAF><WBAN>.csv``
redirige al espejo publico de NOAA en AWS (``noaa-global-hourly-pds``), que se usa
directamente. Lista de estaciones: ``isd-history.csv``. ONI: NOAA CPC ``oni.ascii.txt``.

Los archivos descargados son datos no confiables: se guardan como texto en su propio
directorio y solo se leen con pandas.

Uso::

    uv run python -m experiments.a4_externo.download --out /home/cvelasquez/tdew_timesfm/a4
"""

from __future__ import annotations

import argparse
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

HISTORY_URL = "https://www.ncei.noaa.gov/pub/data/noaa/isd-history.csv"
HOURLY_URL = "https://noaa-global-hourly-pds.s3.amazonaws.com/{year}/{station}.csv"
ONI_URL = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"
YEARS = range(2009, 2021)

logger = logging.getLogger("a4.download")


def _get(url: str, dest: Path, *, retries: int = 3) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=120) as resp, open(tmp, "wb") as fh:
                fh.write(resp.read())
            tmp.replace(dest)
            return True
        except urllib.error.HTTPError as exc:
            if exc.code in (403, 404):
                return False
            logger.warning("%s: HTTP %s (intento %d)", url, exc.code, attempt + 1)
        except (urllib.error.URLError, TimeoutError) as exc:
            logger.warning("%s: %s (intento %d)", url, exc, attempt + 1)
        time.sleep(5 * (attempt + 1))
    return False


def peru_stations(history: Path, first_year: int = YEARS[0]) -> pd.DataFrame:
    """Estaciones con CTRY=PE cuyo periodo de registro alcanza ``first_year``."""
    hist = pd.read_csv(history, dtype=str)
    pe = hist[hist["CTRY"] == "PE"].copy()
    pe = pe[pe["END"].astype(int) >= first_year * 10000 + 101]
    pe["station"] = pe["USAF"] + pe["WBAN"]
    for col in ("LAT", "LON", "ELEV(M)"):
        pe[col] = pd.to_numeric(pe[col], errors="coerce")
    return pe.reset_index(drop=True)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    meta = args.out / "isd_meta"
    raw = args.out / "isd_raw"
    meta.mkdir(parents=True, exist_ok=True)
    raw.mkdir(parents=True, exist_ok=True)
    _get(HISTORY_URL, meta / "isd-history.csv")
    _get(ONI_URL, meta / "oni.ascii.txt")
    stations = peru_stations(meta / "isd-history.csv")
    stations.to_csv(meta / "stations_pe.csv", index=False)
    def fetch(job):
        st, year = job
        dest = raw / str(year) / f"{st}.csv"
        dest.parent.mkdir(exist_ok=True)
        ok = _get(HOURLY_URL.format(year=year, station=st), dest)
        logger.info("%s %d %s", st, year, ok)
        return {"station": st, "year": year, "ok": ok, "bytes": dest.stat().st_size if ok else 0}

    jobs = [(st, year) for st in stations["station"] for year in YEARS]
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(fetch, jobs))
    pd.DataFrame(rows).to_csv(meta / "download_log.csv", index=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
