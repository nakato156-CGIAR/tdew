"""La localización debe medir errores pareados, aunque los histogramas coincidan."""
import numpy as np
import pandas as pd
import json
from pathlib import Path
import pyarrow.parquet as pq
import pytest

from experiments.timesfm.artifact_errores_celdas import error_statistics
from experiments.timesfm.kl import DEFAULT_PALACIOS, DEFAULT_TFM


def test_equal_histograms_can_have_large_daily_errors():
    frame = pd.DataFrame({'ID': [1, 1], 'FECHA': pd.to_datetime(['2013-01-01', '2013-01-02']),
                          'obs': [20., 24.], 'timesfm': [24., 20.]})
    annual, daily = error_statistics(frame, 4.)
    assert sorted(frame.obs) == sorted(frame.timesfm)
    assert annual.iloc[0].max_error == 4.
    assert annual.iloc[0].rmse == 4.
    assert annual.iloc[0].mae == 4.
    assert annual.iloc[0].bias == 0.
    assert annual.iloc[0].extreme == 2
    assert daily.error.tolist() == [4., -4.]


def test_peak_retains_date_observation_prediction_and_fixed_threshold():
    frame = pd.DataFrame({'ID': [1, 1, 1, 1, 2],
                          'FECHA': pd.to_datetime(['2013-01-01', '2013-02-02', '2014-01-01', '2014-02-02', '2013-01-01']),
                          'obs': [10., 10., 10., 10., -10.], 'timesfm': [10., 15., 13., 6., -8.]})
    annual, _ = error_statistics(frame, 4.)
    a = annual.set_index(['ID', 'year'])
    assert a.loc[(1, 2013), 'extreme'] == 1
    assert a.loc[(1, 2014), 'extreme'] == 1
    assert a.loc[(2, 2013), 'extreme'] == 0
    peak = a.loc[(1, 2014)]
    assert peak.FECHA == pd.Timestamp('2014-02-02')
    assert peak.obs == 10. and peak.timesfm == 6. and peak.error == -4.
    assert np.isclose(peak.rmse, np.sqrt((3.**2 + 4.**2) / 2))
    assert a.n.sum() == len(frame)


@pytest.mark.skipif(not DEFAULT_PALACIOS.exists() or not DEFAULT_TFM.exists(), reason='faltan predicciones originales')
def test_published_peaks_and_annual_errors_match_original_daily_pairs():
    path = Path('reports/timesfm_benchmark/artifact/datos_errores_celdas.js')
    if not path.exists():
        pytest.skip('faltan los datos generados')
    data = json.loads(path.read_text().removeprefix('window.D_ERRORS=').strip().removesuffix(';'))
    assert len(data['cells']) == data['meta']['cells'] == 8272
    assert all(c['depto'] != 'fuera_peru' for c in data['cells'])
    warm = max((c for c in data['cells'] if c['warm']), key=lambda c: c['overall']['max_error'])
    worst = next(c for c in data['cells'] if c['id'] == data['worst_id'])
    ids = [warm['id'], worst['id']]
    obs = pq.read_table(DEFAULT_PALACIOS, columns=['ID', 'FECHA', 'TD_obs'], filters=[('ID', 'in', ids)]).to_pandas()
    pred = pq.read_table(DEFAULT_TFM, columns=['ID', 'FECHA', 'pred'], filters=[('ID', 'in', ids)]).to_pandas()
    pairs = obs.merge(pred, on=['ID', 'FECHA'], validate='one_to_one')
    for c in [warm, worst]:
        for i, year in enumerate(data['years']):
            a = pairs[(pairs.ID == c['id']) & (pairs.FECHA.dt.year == year)]
            error = a.pred.astype('float64') - a.TD_obs.astype('float64')
            assert len(a) == c['n'][i]
            assert int((error.abs() >= data['meta']['threshold']).sum()) == c['extreme'][i]
            assert np.isclose(np.sqrt(np.mean(error ** 2)), c['rmse'][i], atol=5.1e-6, rtol=0)
            assert np.isclose(error.abs().max(), c['max_error'][i], atol=5.1e-6, rtol=0)
            day, observed, predicted, signed_error = c['peaks'][i]
            row = a[a.FECHA == pd.Timestamp(day)].iloc[0]
            assert np.isclose(row.TD_obs, observed, atol=5.1e-5, rtol=0)
            assert np.isclose(row.pred, predicted, atol=5.1e-5, rtol=0)
            assert np.isclose(row.pred - float(row.TD_obs), signed_error, atol=5.1e-5, rtol=0)
