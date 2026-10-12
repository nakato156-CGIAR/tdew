"""Frozen date boundaries and guards for the reconstruction experiments."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd


class Protocol(str, Enum):
    DEV_A = "dev_a"
    DEV_B = "dev_b"
    LL4 = "ll4"
    PRODUCTION = "production"


@dataclass(frozen=True)
class ProtocolSpec:
    name: Protocol
    train_start: pd.Timestamp
    train_end: pd.Timestamp
    hidden_start: pd.Timestamp
    hidden_end: pd.Timestamp
    panel_cells_per_department: int | None
    sealed: bool = False

    @property
    def horizon_days(self) -> int:
        return int((self.hidden_end - self.hidden_start).days) + 1

    def train_mask(self, dates: pd.Series) -> pd.Series:
        values = pd.to_datetime(dates)
        return (values >= self.train_start) & (values <= self.train_end)

    def hidden_mask(self, dates: pd.Series) -> pd.Series:
        values = pd.to_datetime(dates)
        return (values >= self.hidden_start) & (values <= self.hidden_end)


_SPECS = {
    Protocol.DEV_A: ProtocolSpec(
        Protocol.DEV_A, pd.Timestamp("1981-01-01"), pd.Timestamp("2004-12-31"),
        pd.Timestamp("2005-01-01"), pd.Timestamp("2008-12-31"), 512,
    ),
    Protocol.DEV_B: ProtocolSpec(
        Protocol.DEV_B, pd.Timestamp("1981-01-01"), pd.Timestamp("2008-12-31"),
        pd.Timestamp("2009-01-01"), pd.Timestamp("2012-12-31"), 512,
    ),
    Protocol.LL4: ProtocolSpec(
        Protocol.LL4, pd.Timestamp("1981-01-01"), pd.Timestamp("2012-12-31"),
        pd.Timestamp("2013-01-01"), pd.Timestamp("2016-12-31"), 2048, sealed=True,
    ),
    Protocol.PRODUCTION: ProtocolSpec(
        Protocol.PRODUCTION, pd.Timestamp("1981-01-01"), pd.Timestamp("2016-12-31"),
        pd.Timestamp("2017-01-01"), pd.Timestamp("2020-12-31"), None,
    ),
}


def protocol_spec(value: Protocol | str) -> ProtocolSpec:
    return _SPECS[Protocol(value)]


def require_protocol_access(value: Protocol | str, *, unlock_ll4: bool = False) -> ProtocolSpec:
    """Return a protocol spec, refusing accidental access to the final holdout."""
    spec = protocol_spec(value)
    if spec.sealed and not unlock_ll4:
        raise PermissionError("ll4 is sealed; pass unlock_ll4=True only after freezing the winner")
    return spec


def horizon_year(dates: pd.Series, spec: ProtocolSpec) -> pd.Series:
    dates = pd.to_datetime(dates)
    if not bool(((dates >= spec.hidden_start) & (dates <= spec.hidden_end)).all()):
        raise ValueError("All dates must belong to the protocol hidden interval")
    return dates.dt.year - spec.hidden_start.year + 1
