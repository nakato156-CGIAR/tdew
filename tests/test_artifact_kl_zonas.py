"""Dirección y magnitud se mantienen separadas; las KL locales no son aditivas."""
import json
from pathlib import Path

import numpy as np
import pytest
import pyarrow.parquet as pq

from experiments.timesfm.artifact_kl_zonas import distribution_summary
from experiments.timesfm.kl import DEFAULT_PALACIOS, DEFAULT_TFM, _hist

PATH=Path('reports/timesfm_benchmark/artifact/datos_kl_zonas.js')


def payload():
    return json.loads(PATH.read_text().split('=',1)[1].rstrip(';\n'))


def test_misma_media_no_implica_misma_distribucion():
    r=distribution_summary([2,0,2],[0,4,0],4,8,8)
    assert r['kl']>0 and r['delta']==0


def test_direccion_no_se_deduce_de_kl():
    cold=distribution_summary([0,4,0],[4,0,0],4,8,4)
    warm=distribution_summary([0,4,0],[0,0,4],4,8,12)
    assert cold['delta']==-1 and warm['delta']==1
    np.testing.assert_allclose(cold['kl'],warm['kl'])


def test_poblacion_cronologia_y_agregacion_de_medias():
    d=payload()
    assert d['years']==[2013,2014,2015,2016]
    assert len(d['cells'])==8272
    assert all(c['depto']!='fuera_peru' for c in d['cells'])
    total=d['national']['total']
    assert total['n']==12085392==sum(c['total']['n'] for c in d['cells'])
    assert sum(r['total']['n'] for r in d['regions'])==total['n']
    for scope in [d['national'],*d['regions'],*d['cells']]:
        assert len(scope['annual'])==4
        assert sum(r['n'] for r in scope['annual'])==scope['total']['n']
        np.testing.assert_allclose(sum(r['n']*r['delta'] for r in scope['annual'])/scope['total']['n'],scope['total']['delta'],atol=1e-12)
        for r in [scope['total'],*scope['annual']]:
            assert r['kl']>=-1e-12
            np.testing.assert_allclose(r['delta'],r['pred_mean']-r['obs_mean'],atol=1e-12)
    old=json.loads(Path('reports/timesfm_benchmark/artifact/datos_kl_localizacion.js').read_text().split('=',1)[1].rstrip(';\n'))
    np.testing.assert_allclose(total['kl'],sum(old['kl']['bins']['aporte_timesfm']),atol=1e-12)
    assert d['years'][np.argmax([r['kl'] for r in d['national']['annual']])]==2015


@pytest.mark.skipif(not DEFAULT_PALACIOS.exists() or not DEFAULT_TFM.exists(),reason='faltan predicciones originales')
def test_dos_celdas_contra_predicciones_originales():
    d=payload(); cells=[d['cells'][0],d['cells'][-1]];ids=[c['id'] for c in cells]
    obs=pq.read_table(DEFAULT_PALACIOS,columns=['ID','FECHA','TD_obs'],filters=[('ID','in',ids)]).to_pandas()
    pred=pq.read_table(DEFAULT_TFM,columns=['ID','FECHA','pred'],filters=[('ID','in',ids)]).to_pandas()
    pairs=obs.merge(pred,on=['ID','FECHA'],validate='one_to_one')
    for c in cells:
        a=pairs[pairs.ID==c['id']]
        for j in [None,0,1,2,3]:
            b=a if j is None else a[a.FECHA.dt.year==d['years'][j]]
            o=b.TD_obs.to_numpy();q=b.pred.to_numpy()
            expected=distribution_summary(_hist(o,.5)[0],_hist(q,.5)[0],len(b),o.astype('float64').sum(),q.astype('float64').sum())
            actual=c['total'] if j is None else c['annual'][j]
            assert actual['n']==len(b)
            for key in ['kl','delta','obs_mean','pred_mean']:
                np.testing.assert_allclose(actual[key],expected[key],atol=1e-12)
