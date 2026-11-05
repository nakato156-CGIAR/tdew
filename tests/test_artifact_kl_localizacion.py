"""La localización debe conservar el aporte del histograma global."""
import json
from pathlib import Path

import numpy as np

from experiments.timesfm.artifact_kl_localizacion import bin_weights, contributions

ROOT = Path(__file__).resolve().parents[1]


def test_aportes_aditivos_con_compensacion():
    obs = np.array([[3, 0], [1, 2], [0, 4]])
    pred = np.array([[0, 3], [2, 1], [0, 4]])
    _, _, terms, weights, z = bin_weights(obs.sum(0), pred.sum(0))
    a = contributions(obs, pred, weights, z)
    np.testing.assert_allclose(a.sum(0), terms)
    np.testing.assert_array_equal(a[2], [0, 0])
    assert a[0, 0] > 0 and a[1, 0] < 0


def test_permutacion_con_error_diario_no_aporta_a_kl():
    obs = np.array([0, 0, 20, 20])
    pred = obs[::-1]
    assert np.abs(obs - pred).mean() == 20
    oh = np.histogram(obs, bins=[-1, 10, 21])[0]
    qh = np.histogram(pred, bins=[-1, 10, 21])[0]
    _, _, terms, weights, z = bin_weights(oh, qh)
    np.testing.assert_array_equal(terms, [0, 0])
    np.testing.assert_array_equal(contributions(oh, qh, weights, z), [0, 0])


def test_publicacion_reconcilia_celdas_anios_y_curva():
    src = (ROOT / 'reports/timesfm_benchmark/artifact/datos_kl_localizacion.js').read_text()
    d = json.loads(src.split('=', 1)[1].rstrip(';\n'))
    assert d['years'] == [2013, 2014, 2015, 2016]
    assert len(d['cells']) == 8272
    assert all(c['depto'] != 'fuera_peru' for c in d['cells'])
    n = sum(sum(c['n']) for c in d['cells'])
    assert n == d['kl']['n'] == 12085392
    z = n + 140 * .5
    for k, peak in enumerate(d['peaks']):
        obs = np.array([c['obs'][k] for c in d['cells']])
        pred = np.array([c['pred'][k] for c in d['cells']])
        assert obs.sum() == peak['obs'] and pred.sum() == peak['pred']
        a = contributions(obs, pred, peak['weight'], z)
        np.testing.assert_allclose(a.sum(0), peak['years'], atol=1e-14)
        np.testing.assert_allclose(a.sum(), peak['term'], atol=1e-14)
        np.testing.assert_allclose(peak['term'], d['kl']['bins']['aporte_timesfm'][peak['bin']], atol=1e-14)
    for method in ['timesfm', 'palacios']:
        row = next(r for r in d['kl']['grupos'] if r['group_kind'] == 'todo' and r['method'] == method and str(r['bin_width']) == '0.5')
        np.testing.assert_allclose(sum(d['kl']['bins']['aporte_' + method]), row['kl_obs_method'], atol=1e-12)
        np.testing.assert_allclose(sum(d['kl']['bins'][method]), 1, atol=1e-12)


def test_conteos_de_dos_celdas_contra_predicciones_originales():
    import pyarrow.parquet as pq
    import pytest
    from experiments.timesfm.kl import DEFAULT_PALACIOS, DEFAULT_TFM
    if not DEFAULT_PALACIOS.exists() or not DEFAULT_TFM.exists():
        pytest.skip('faltan predicciones originales')
    src = (ROOT / 'reports/timesfm_benchmark/artifact/datos_kl_localizacion.js').read_text()
    d = json.loads(src.split('=', 1)[1].rstrip(';\n'))
    chosen = [max(d['peaks'], key=lambda p: p['term'])['top_id'], min(d['peaks'], key=lambda p: p['term'])['top_id']]
    obs = pq.read_table(DEFAULT_PALACIOS, columns=['ID', 'FECHA', 'TD_obs'], filters=[('ID', 'in', chosen)]).to_pandas()
    pred = pq.read_table(DEFAULT_TFM, columns=['ID', 'FECHA', 'pred'], filters=[('ID', 'in', chosen)]).to_pandas()
    pairs = obs.merge(pred, on=['ID', 'FECHA'], validate='one_to_one')
    for c in (c for c in d['cells'] if c['id'] in chosen):
        for j, year in enumerate(d['years']):
            a = pairs[(pairs.ID == c['id']) & (pairs.FECHA.dt.year == year)]
            assert len(a) == c['n'][j]
            for k, p in enumerate(d['peaks']):
                assert int(((a.TD_obs >= p['lo']) & (a.TD_obs < p['hi'])).sum()) == c['obs'][k][j]
                assert int(((a.pred >= p['lo']) & (a.pred < p['hi'])).sum()) == c['pred'][k][j]
