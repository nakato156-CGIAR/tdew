"""Raices de datos del benchmark TimesFM, configurables por variable de entorno.

Los valores por defecto son las rutas de la estacion de trabajo donde se corrio el
benchmark. Para reproducirlo en otra maquina basta con exportar:

- ``TDEW_RES``: almacen de produccion de Palacios (``results_tuning``), solo lectura.
- ``TDEW_TIMESFM_WORK``: directorio de trabajo de TimesFM (predicciones e intermedios).
- ``TDEW_RECONSTRUCTION_WORK``: directorio de trabajo del protocolo de reconstruccion
  (panel departamental de la TCN).
"""

from __future__ import annotations

import os
from pathlib import Path

RES = Path(os.environ.get("TDEW_RES", "/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning"))
WORK = Path(os.environ.get("TDEW_TIMESFM_WORK", "/home/cvelasquez/tdew_timesfm"))
RECONSTRUCTION_WORK = Path(os.environ.get("TDEW_RECONSTRUCTION_WORK", "/home/cvelasquez/tdew_reconstruction"))
