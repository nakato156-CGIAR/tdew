"""
visualizations.app

Streamlit dashboard for looking at the PISCO raster data directly (no model
involved) — a daily/annual map and the per-cell climatology, for whatever
variables and years currently exist under ``Data/silver``. Both views read
straight from silver on demand (see ``visualizations/data_access.py``); no
gold table is required.

Two views only, on purpose: the other two originally discussed (SENAMHI
41-zone map, TD real-vs-predicted for 2017-2020) need inputs that don't
exist in this repo yet — the ``clasif_clima_peru.zip`` zone shapefile used by
``HPC_code_tunning/zones.py``, and TD predictions from
``tdew_estimation``/``Local/run_pipeline.sh`` (``Data/gold`` has no
predictions materialized). Add them as new tabs here once those inputs land.

Usage
-----
streamlit run visualizations/raster/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# ``streamlit run`` puts this file's own directory on sys.path, not the repo
# root, so the ``visualizations.*`` package imports below need a hand.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
import streamlit as st

from visualizations.raster.data_access import list_variables, list_years, load_climatology_day, load_day
from visualizations.raster.plotting import draw_raster
from visualizations.raster.render_video import build_year_video, render_path

st.set_page_config(page_title="TDEW — Vista raster", layout="wide")
st.title("TDEW — Vista raster de la data (silver)")


variables = list_variables()
if not variables:
    st.error("No hay variables en Data/silver todavía. Corre `python -m pipeline.silver` primero.")
    st.stop()

with st.sidebar:
    var = st.selectbox("Variable", variables)
    years = list_years(var)
    if not years:
        st.error(f"No hay años de '{var}' en Data/silver.")
        st.stop()
    year = st.selectbox("Año", years)

tab_daily, tab_clim = st.tabs(["Mapa diario / Video del año", "Climatología"])

with tab_daily:
    jan1 = pd.Timestamp(year=year, month=1, day=1)
    dec31 = pd.Timestamp(year=year, month=12, day=31)
    date = pd.Timestamp(
        st.slider("Día", min_value=jan1.to_pydatetime(), max_value=dec31.to_pydatetime(), value=jan1.to_pydatetime())
    )

    raster = load_day(var, date)
    if raster is None:
        st.warning(f"No hay datos de {var} para {date.strftime('%Y-%m')} en silver.")
    else:
        st.pyplot(draw_raster(raster, f"{var.upper()} — {date.date()}", var.upper()))

    st.divider()
    st.subheader(f"Video del año {year}")
    existing = render_path(var, year)
    if existing.exists():
        st.video(str(existing))
        if st.button("Regenerar video"):
            with st.spinner("Generando video..."):
                out_path = build_year_video(var, year, overwrite=True)
            st.video(str(out_path))
    else:
        if st.button("Generar video del año"):
            with st.spinner("Generando video (puede tardar varios minutos para todo el año)..."):
                out_path = build_year_video(var, year)
            st.video(str(out_path))

with tab_clim:
    doy = st.slider("Día del año (1-366)", min_value=1, max_value=366, value=1)
    with st.spinner("Calculando climatología..."):
        clim_raster = load_climatology_day(var, doy)
    if clim_raster is None:
        st.warning(f"No hay datos de '{var}' en Data/silver para calcular la climatología del día {doy}.")
    else:
        st.pyplot(draw_raster(clim_raster, f"{var.upper()}_clim — día del año {doy}", f"{var.upper()}_clim"))
