"""KL local y anual de distribuciones completas, con dirección del cambio medio."""
import json
from pathlib import Path

import numpy as np

from .artifact_kl_localizacion import bin_index
from .kl import ALPHA, DEFAULT_PALACIOS, DEFAULT_TFM, load_pairs

ROOT = Path('reports/timesfm_benchmark')


def distribution_summary(obs, pred, n, obs_sum, pred_sum):
    """KL(obs||TimesFM) y diferencia de medias; son medidas independientes."""
    p = (np.asarray(obs, dtype='float64') + ALPHA)
    q = (np.asarray(pred, dtype='float64') + ALPHA)
    p /= p.sum(axis=-1, keepdims=True)
    q /= q.sum(axis=-1, keepdims=True)
    return {'n': int(n), 'kl': float((p * np.log(p/q)).sum()),
            'delta': float((pred_sum-obs_sum)/n),
            'obs_mean': float(obs_sum/n), 'pred_mean': float(pred_sum/n)}


def main():
    src = ROOT / 'artifact/datos_kl_localizacion.js'
    base = json.loads(src.read_text().split('=',1)[1].rstrip(';\n'))
    cells = base['cells']; ids = np.array([c['id'] for c in cells]); years=base['years']
    frame = load_pairs(DEFAULT_PALACIOS, DEFAULT_TFM)
    frame = frame[frame.ID.isin(ids)].reset_index(drop=True)
    ci = np.searchsorted(ids, frame.ID.to_numpy())
    yi = np.searchsorted(years, frame.FECHA.dt.year.to_numpy())
    gi = ci * len(years) + yi; size=len(ids)*len(years); nb=140
    n=np.bincount(gi,minlength=size).reshape(len(ids),len(years))
    hist=[]; sums=[]
    for col in ['obs','timesfm']:
        values=frame[col].to_numpy()
        hist.append(np.bincount(gi*nb+bin_index(values),minlength=size*nb).reshape(len(ids),len(years),nb))
        sums.append(np.bincount(gi,weights=values.astype('float64'),minlength=size).reshape(len(ids),len(years)))
    def summarize(mask):
        h=[x[mask].sum(axis=0) for x in hist]; ns=n[mask].sum(axis=0); ss=[x[mask].sum(axis=0) for x in sums]
        yearly=[distribution_summary(h[0][j],h[1][j],ns[j],ss[0][j],ss[1][j]) for j in range(len(years))]
        total=distribution_summary(h[0].sum(0),h[1].sum(0),ns.sum(),ss[0].sum(),ss[1].sum())
        return {'total':total,'annual':yearly}
    rows=[]
    for i,c in enumerate(cells):
        summary=summarize(np.array([i]))
        rows.append({key:c[key] for key in ['id','lon','lat','depto','zona']}|summary)
    regions=[]
    for dep in sorted(set(c['depto'] for c in cells)):
        mask=np.array([i for i,c in enumerate(cells) if c['depto']==dep])
        regions.append({'name':dep,'cells':len(mask),**summarize(mask)})
    national=summarize(np.arange(len(cells)))
    expected=sum(base['kl']['bins']['aporte_timesfm'])
    assert np.isclose(national['total']['kl'],expected,atol=1e-12,rtol=0)
    assert sum(r['total']['n'] for r in regions)==national['total']['n']==12085392
    for j in range(4):
        assert sum(r['annual'][j]['n'] for r in regions)==national['annual'][j]['n']
    payload={'years':years,'cells':rows,'regions':regions,'national':national,'outlines':base['outlines'],
        'meta':{'scope':'Perú','bin_width':.5,'alpha':ALPHA,'bins':140,'range':[-20,50],
        'kl':'KL(obs||TimesFM), recalculada para cada celda, departamento y año; no aditiva',
        'direction':'Media TimesFM menos media observada, en °C, sin discretizar ni suavizar',
        'sources':[str(DEFAULT_PALACIOS),str(DEFAULT_TFM)],'n':len(frame)}}
    dest=ROOT/'artifact/datos_kl_zonas.js'
    dest.write_text('window.D_KL_ZONES='+json.dumps(payload,ensure_ascii=False,separators=(',',':'),allow_nan=False)+';\n')
    out=ROOT/'kl_zonas';out.mkdir(exist_ok=True)
    (out/'resumen.json').write_text(json.dumps({k:v for k,v in payload.items() if k not in ['cells','outlines']},ensure_ascii=False,indent=2)+'\n')
    print('NACIONAL',national,flush=True)
    print('REGIONES',sorted([(r['name'],r['total']['kl'],r['total']['delta']) for r in regions],key=lambda x:-x[1])[:8],flush=True)
    print('LISTO',dest.stat().st_size,flush=True)


if __name__=='__main__':
    main()
