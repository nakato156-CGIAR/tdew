"""Las variantes zero-shot de TimesFM, como datos y no como ramas de codigo.

Cada variante fija lo unico que puede fijarse sin entrenar: que serie se le pide
predecir, que covariables recibe, cuanto contexto ve y que interruptores de
inferencia se activan. Ninguna depende del resultado de otra, asi que se pueden
correr en cualquier orden o en paralelo.

La covariable es TMIN y solo TMIN en el nivel nacional porque es exactamente la
informacion que consume el metodo de Palacios (`Td ~ f(Tmin)` por zona y dia del
anio): igualarla hace que la comparacion mida el modelo y no el acceso a datos.
"""

from __future__ import annotations

from dataclasses import dataclass, field

TIMESFM_30 = "google/timesfm-3.0-pytorch"
# Snapshot de Hugging Face con el que se corrio todo el benchmark (cache local de la estacion de
# trabajo, octubre de 2026). Fijarlo evita que una subida nueva al mismo repo cambie los pesos.
CHECKPOINT_REVISION = "43046b85ec22d584a13f8098c2ed39c889e129c2"


@dataclass(frozen=True)
class Variant:
    """Una configuracion zero-shot completa."""

    key: str
    target: str  # "TD" o "TD_anom"
    covariates: tuple[str, ...]  # subconjunto de ("TMIN", "TMIN_anom", "DOY")
    context_start_year: int
    autoregressive: bool = False
    symmetric_averaging: bool = False
    znorm: bool = False
    checkpoint: str = TIMESFM_30
    note: str = ""

    @property
    def family(self) -> str:
        return "timesfm-3.0"

    @property
    def n_covariate_channels(self) -> int:
        """Canales reales entregados al modelo (DOY aporta seno y coseno)."""
        return sum(2 if name == "DOY" else 1 for name in self.covariates)

    @property
    def target_type(self) -> str:
        """Vocabulario compartido con tdew_estimation.provenance.MetricProvenance."""
        return "td_anomaly" if self.target == "TD_anom" else "td_raw"

    @property
    def climatology_used(self) -> bool:
        """La climatologia entra si el objetivo o alguna covariable estan en anomalia."""
        return self.target_type == "td_anomaly" or any(
            name.endswith("_anom") for name in self.covariates
        )

    @property
    def inputs(self) -> tuple[str, ...]:
        """Covariables exogenas entregadas al modelo; alias de ``covariates`` con el
        vocabulario de ``tdew_estimation.provenance.MetricProvenance.inputs``."""
        return self.covariates

    @property
    def climatology_role(self) -> str | None:
        if not self.climatology_used:
            return None
        return "target_anomaly_base" if self.target_type == "td_anomaly" else "input_covariate"

    def describe(self) -> str:
        cov = ", ".join(self.covariates) if self.covariates else "sin covariables"
        return f"{self.key}: objetivo {self.target}; {cov}; contexto desde {self.context_start_year}"


VARIANTS: tuple[Variant, ...] = (
    Variant(
        key="uni_td_full",
        target="TD",
        covariates=(),
        context_start_year=1981,
        note="Univariante puro sobre Td crudo. Mide cuanta senal temporal queda a 1.461 dias.",
    ),
    Variant(
        key="uni_anom_full",
        target="TD_anom",
        covariates=(),
        context_start_year=1981,
        note="Univariante sobre la anomalia: le quita el ciclo estacional al objetivo.",
    ),
    Variant(
        key="tmin_td_full",
        target="TD",
        covariates=("TMIN",),
        context_start_year=1981,
        note="La comparacion justa contra Palacios: misma covariable, mismo horizonte.",
    ),
    Variant(
        key="tmin_anom_full",
        target="TD_anom",
        covariates=("TMIN_anom",),
        context_start_year=1981,
        note="Igual que la anterior pero con todo expresado en anomalias.",
    ),
    Variant(
        key="tmin_doy_td_full",
        target="TD",
        covariates=("TMIN", "DOY"),
        context_start_year=1981,
        note="TimesFM no tiene indicador de frecuencia; aqui el dia del anio se le entrega a mano.",
    ),
    Variant(
        key="tmin_td_med",
        target="TD",
        covariates=("TMIN",),
        context_start_year=2002,
        note="Contexto desde 2002: 11 anios (4.018 dias) en ll4; mas largo en ll1 y ll2.",
    ),
    Variant(
        key="tmin_td_short",
        target="TD",
        covariates=("TMIN",),
        context_start_year=2011,
        note="Contexto desde 2011: 2 anios (731 dias, 2012 es bisiesto) en ll4; mas largo en ll1 y ll2. El minimo para que el ciclo anual sea visible dos veces.",
    ),
    Variant(
        key="tmin_td_symavg",
        target="TD",
        covariates=("TMIN",),
        context_start_year=1981,
        symmetric_averaging=True,
        note="Promediado simetrico: duplica el computo y corrige asimetria de signo.",
    ),
    Variant(
        key="tmin_td_znorm",
        target="TD",
        covariates=("TMIN",),
        context_start_year=1981,
        znorm=True,
        note="z-score externo ademas del RevIN interno; reescala tambien las covariables.",
    ),
)

BY_KEY: dict[str, Variant] = {v.key: v for v in VARIANTS}


def variant(key: str) -> Variant:
    if key not in BY_KEY:
        raise KeyError(f"variante desconocida: {key!r}; hay {sorted(BY_KEY)}")
    return BY_KEY[key]


def parse_keys(spec: str) -> list[str]:
    """``"all"`` o una lista separada por comas."""
    if spec.strip().lower() == "all":
        return [v.key for v in VARIANTS]
    keys = [part.strip() for part in spec.split(",") if part.strip()]
    for key in keys:
        variant(key)
    return keys
