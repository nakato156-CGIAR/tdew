"""Localización aditiva de los aportes de los bins a KL(obs || TimesFM), solo Perú.

Para cada bin se fija el mismo peso global w = p*log(p/q)/(p-q). El aporte de un
subgrupo es (O_g-Q_g)*w/(N+B*alpha). Se reconcilia exactamente con el aporte del
bin global. Es un aporte firmado al pico global, no la KL calculada por celda.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .kl import ALPHA, BIN_COARSE, DEFAULT_PALACIOS, DEFAULT_TFM, HI, LO, _edges, _hist, compute, load_pairs
from .kl_calido import DEFAULT_GEO, DEFAULT_STATIC, cell_table
from .real_compare import DEFAULT_SUPPORT, DEFAULT_ZONE

OUT = Path('reports/timesfm_benchmark/kl_localizacion')


def bin_weights(obs_counts, pred_counts, alpha=ALPHA):
    """Peso no negativo que transforma el balance de cuentas en aporte KL exacto."""
    obs_counts = np.asarray(obs_counts, dtype='float64')
    pred_counts = np.asarray(pred_counts, dtype='float64')
    assert obs_counts.sum() == pred_counts.sum()
    z = float(obs_counts.sum() + alpha * len(obs_counts))
    p, q = (obs_counts + alpha) / z, (pred_counts + alpha) / z
    terms = p * np.log(p / q)
    weight = np.ones_like(p)
    different = obs_counts != pred_counts
    weight[different] = terms[different] / ((obs_counts[different] - pred_counts[different]) / z)
    return p, q, terms, weight, z


def contributions(obs, pred, weight, normalizer):
    """Aportes firmados; no se renormalizan los grupos ni se calcula una KL local."""
    return (np.asarray(obs, dtype='float64') - np.asarray(pred, dtype='float64')) * weight / normalizer


def bin_index(values):
    return np.floor((np.clip(values, LO, np.nextafter(HI, LO)) - LO) / BIN_COARSE).astype('int64')


def main():
    frame = load_pairs(DEFAULT_PALACIOS, DEFAULT_TFM)
    cells = cell_table(np.sort(frame.ID.unique()), DEFAULT_ZONE, DEFAULT_SUPPORT, DEFAULT_STATIC, DEFAULT_GEO)
    cells = cells[cells.depto != 'fuera_peru'].sort_values('ID').reset_index(drop=True)
    frame = frame[frame.ID.isin(cells.ID)].reset_index(drop=True)
    assert not frame.duplicated(['ID', 'FECHA']).any()
    assert np.isfinite(frame[['obs', 'timesfm', 'palacios']].to_numpy()).all()
    year = frame.FECHA.dt.year.to_numpy()
    years = sorted(int(v) for v in np.unique(year))
    cell_i = np.searchsorted(cells.ID.to_numpy(), frame.ID.to_numpy())
    group = cell_i * len(years) + np.searchsorted(years, year)
    size = len(cells) * len(years)
    n = np.bincount(group, minlength=size).reshape(len(cells), len(years))
    obs_bin, pred_bin = bin_index(frame.obs.to_numpy()), bin_index(frame.timesfm.to_numpy())
    edges = _edges(BIN_COARSE)
    nb = len(edges) - 1
    h_obs, _ = _hist(frame.obs.to_numpy(), BIN_COARSE)
    h_pred, _ = _hist(frame.timesfm.to_numpy(), BIN_COARSE)
    np.testing.assert_array_equal(h_obs, np.bincount(obs_bin, minlength=nb))
    np.testing.assert_array_equal(h_pred, np.bincount(pred_bin, minlength=nb))
    p, q, terms, weight, z = bin_weights(h_obs, h_pred)
    selected = sorted(set(np.argsort(terms)[-3:].tolist() + np.argsort(terms)[:3].tolist()))
    selected = [b for b in selected if abs(terms[b]) > 1e-14]
    obs = np.stack([np.bincount(group[obs_bin == b], minlength=size).reshape(len(cells), len(years)) for b in selected], axis=1)
    pred = np.stack([np.bincount(group[pred_bin == b], minlength=size).reshape(len(cells), len(years)) for b in selected], axis=1)
    all_a = np.stack([contributions(obs[:, k, :], pred[:, k, :], weight[b], z) for k, b in enumerate(selected)], axis=1)
    np.testing.assert_array_equal(obs.sum(axis=(0, 2)), h_obs[selected])
    np.testing.assert_array_equal(pred.sum(axis=(0, 2)), h_pred[selected])
    np.testing.assert_allclose(all_a.sum(axis=(0, 2)), terms[selected], rtol=1e-12, atol=1e-15)
    # Curvas superiores y tablas sobre exactamente los mismos pares peruanos.
    zone = pd.read_parquet(DEFAULT_ZONE, columns=['ID', 'zone_id']).set_index('ID').zone_id
    tier = cells.set_index('ID').tier
    groups, _ = compute(frame, tier, zone)
    for method in ['timesfm', 'palacios']:
        h, _ = _hist(frame[method].to_numpy(), BIN_COARSE)
        _, _, t, _, _ = bin_weights(h_obs, h)
        ref = groups[(groups.group_kind == 'todo') & (groups.method == method) & (groups.bin_width == '0.5')]
        assert np.isclose(t.sum(), ref.iloc[0].kl_obs_method, atol=1e-12, rtol=0)
    bins = {'lo': edges[:-1].tolist(), 'hi': edges[1:].tolist(), 'obs': p.tolist()}
    for method in ['timesfm', 'palacios']:
        h, _ = _hist(frame[method].to_numpy(), BIN_COARSE)
        _, density, t, _, _ = bin_weights(h_obs, h)
        bins[method] = density.tolist()
        bins['aporte_' + method] = t.tolist()
    kl = {'grupos': json.loads(groups.to_json(orient='records', double_precision=15)),
          'bins': bins, 'alpha': ALPHA, 'n': len(frame), 'scope': 'Perú'}
    choices = []
    for k, b in enumerate(selected):
        a = all_a[:, k, :]
        direction = 1 if terms[b] > 0 else -1
        by_year = a.sum(axis=0)
        chosen = {'bin': b, 'lo': float(edges[b]), 'hi': float(edges[b + 1]),
                  'p': float(p[b]), 'q': float(q[b]), 'term': float(terms[b]), 'weight': float(weight[b]),
                  'obs': int(h_obs[b]), 'pred': int(h_pred[b]), 'years': by_year.tolist(),
                  'positive': float(a[a * direction > 0].sum()), 'negative': float(a[a * direction < 0].sum())}
        top = int(np.argmax(direction * a.sum(axis=1)))
        chosen['top_id'] = int(cells.iloc[top].ID)
        chosen['top_depto'] = str(cells.iloc[top].depto)
        choices.append(chosen)
        print('PICO', edges[b], edges[b+1], 'aporte', terms[b], 'top', chosen['top_depto'], chosen['top_id'], 'años', by_year, flush=True)
    rows = []
    records = []
    for i, c in enumerate(cells.itertuples(index=False)):
        rows.append({'id': int(c.ID), 'lon': round(float(c.lon), 5), 'lat': round(float(c.lat), 5),
                     'depto': str(c.depto), 'zona': str(c.zone_label), 'n': n[i].tolist(),
                     'obs': obs[i].tolist(), 'pred': pred[i].tolist()})
        for k, b in enumerate(selected):
            for j, y in enumerate(years):
                records.append({'ID': int(c.ID), 'anio': y, 'bin_lo': float(edges[b]), 'bin_hi': float(edges[b+1]),
                                'n': int(n[i,j]), 'obs': int(obs[i,k,j]), 'timesfm': int(pred[i,k,j]),
                                'aporte_kl': float(all_a[i,k,j]), 'depto': str(c.depto), 'zone_label': str(c.zone_label)})
    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(OUT / 'celda_anio_bin.csv', index=False)
    groups.to_csv(OUT / 'kl_by_group_peru.csv', index=False)
    pd.DataFrame({'bin_lo':edges[:-1], 'bin_hi':edges[1:], 'obs':h_obs, 'timesfm':h_pred, 'aporte_kl':terms}).to_csv(OUT / 'hist_peru.csv', index=False)
    meta = {'bead': 'tdew-rey', 'generated_at': datetime.now(timezone.utc).isoformat(),
            'scope': 'Perú', 'n': len(frame), 'cells': len(cells), 'width': BIN_COARSE, 'alpha': ALPHA,
            'normalizer': z, 'n_bins': nb, 'selected_bins': selected,
            'sources': [str(DEFAULT_PALACIOS), str(DEFAULT_TFM), str(DEFAULT_ZONE), str(DEFAULT_GEO)],
            'selection': 'Tres mayores aportes positivos y tres más negativos de la curva KL(obs||TimesFM), bins 0.5°C',
            'attribution': 'A_gb=(O_gb-Q_gb)/(N+B*alpha)*w_b; w_b=p_b*ln(p_b/q_b)/(p_b-q_b), con límite 1 si p_b=q_b',
            'interpretation': 'Aporte firmado al bin de la KL global; no es KL calculada por celda ni error diario',
            'validation': 'Histogramas coinciden con kl._hist; cuentas por celda/año suman las globales; aportes suman cada pico; curva completa suma KL 0.5°C de la tabla, mismos pares de Perú'}
    payload = {'years': years, 'cells': rows, 'peaks': choices, 'kl': kl,
               'outlines': json.loads(DEFAULT_GEO.read_text()), 'meta': meta}
    dest = Path('reports/timesfm_benchmark/artifact/datos_kl_localizacion.js')
    dest.write_text('window.D_KL_SPATIAL=' + json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + ';\n')
    meta['sha256'] = hashlib.sha256(dest.read_bytes()).hexdigest()
    (OUT / 'provenance.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n')
    print('LISTO', len(cells), len(frame), 'bytes', dest.stat().st_size, flush=True)


if __name__ == '__main__':
    main()
