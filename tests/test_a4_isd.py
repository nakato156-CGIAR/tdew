"""Parseo ISD y agregacion diaria de experiments.a4_externo.isd con datos sinteticos."""

import numpy as np
import pandas as pd
import pytest

from experiments.a4_externo import isd


def test_parse_value_handles_missing_and_sign():
    v, qc = isd.parse_value(pd.Series(["+0185,1", "-0032,5", "+9999,9", None, "x"]))
    assert v[0] == pytest.approx(18.5) and qc[0] == "1"
    assert v[1] == pytest.approx(-3.2) and qc[1] == "5"
    assert np.isnan(v[2]) and np.isnan(v[3]) and np.isnan(v[4])


def _frame(times_utc, dews, tmps=None):
    tmps = tmps or ["+0300,1"] * len(dews)
    return pd.DataFrame({"DATE": times_utc, "DEW": dews, "TMP": tmps})


def test_clean_hourly_qc_rules():
    frame = _frame(
        ["2018-01-01T05:00:00"] * 6,
        ["+0150,1", "+0150,2", "+0150,3", "+0150,A", "+9999,9", "+0350,1"],
        ["+0300,1"] * 5 + ["+0200,1"],  # el ultimo: Td 35 > T 20 + 0.5 (sobresaturado)
    )
    out = isd.clean_hourly(frame)
    assert len(out) == 1
    assert out["td"].iloc[0] == pytest.approx(15.0)
    # 05 UTC -> 00 local del mismo dia
    assert out["local"].iloc[0] == pd.Timestamp("2018-01-01 00:00")


def test_daily_block_mean_and_completeness():
    # dia local 2018-01-02 = 05 UTC del 2 a 04 UTC del 3
    times, dews = [], []
    # bloque 00-06 local: 2 horas con 10 y 12 (y un duplicado METAR en la misma hora)
    for h, d in [(5, 100), (5, 100), (6, 120)]:
        times.append(f"2018-01-02T{h:02d}:00:00"); dews.append(f"+{d:04d},1")
    # bloques 06-12, 12-18, 18-24 local: una hora cada uno, 14, 16, 18 C
    for h, d in [(12, 140), (18, 160), (23, 180)]:
        times.append(f"2018-01-02T{h:02d}:00:00"); dews.append(f"+{d:04d},1")
    # dia siguiente: solo de dia (bloques 1 y 2) -> invalido
    for h in (13, 14, 15, 16, 17, 18):
        times.append(f"2018-01-03T{h:02d}:00:00"); dews.append("+0150,1")
    daily = isd.daily_from_hourly(isd.clean_hourly(_frame(times, dews)))
    assert list(daily["FECHA"]) == [pd.Timestamp("2018-01-02")]
    # media de bloques: (11 + 14 + 16 + 18) / 4; la hora duplicada cuenta una vez
    assert daily["TD"].iloc[0] == pytest.approx((11 + 14 + 16 + 18) / 4)
    assert daily["n_hours"].iloc[0] == 5
    assert daily["n_blocks"].iloc[0] == 4


def test_daily_min_hours():
    times = [f"2018-01-02T{h:02d}:00:00" for h in (5, 12, 18, 23)]
    dews = ["+0100,1"] * 4
    hourly = isd.clean_hourly(_frame(times, dews))
    assert len(isd.daily_from_hourly(hourly, min_hours=4)) == 1
    assert len(isd.daily_from_hourly(hourly, min_hours=5)) == 0
