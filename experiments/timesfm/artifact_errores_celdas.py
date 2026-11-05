"""Errores pareados de TimesFM por celda, fecha y año, únicamente dentro del Perú."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from .kl import DEFAULT_PALACIOS, DEFAULT_TFM, load_pairs
from .kl_calido import DEFAULT_GEO, DEFAULT_STATIC, cell_table
from .real_compare import DEFAULT_SUPPORT, DEFAULT_ZONE

OUT = Path('reports/timesfm_benchmark/errores_celdas')
THERMAL_SOURCE = 'https://www.senamhi.gob.pe/load/file/01404SENA-4.pdf'


def error_statistics(frame: pd.DataFrame, threshold: float):
    """Se agregan errores de los mismos días; se conserva la fecha y el signo del pico."""
    frame = frame.copy()
    frame['year'] = frame.FECHA.dt.year.astype('int16')
    frame['error'] = frame.timesfm.astype('float64') - frame.obs.astype('float64')
    frame['abs_error'] = frame.error.abs()
    frame['sq_error'] = frame.error ** 2
    frame['extreme'] = (frame.abs_error >= threshold).astype('int32')
    group = frame.groupby(['ID', 'year'], sort=True)
    annual = group.agg(n=('error', 'size'), mae=('abs_error', 'mean'),
                       mse=('sq_error', 'mean'), bias=('error', 'mean'),
                       max_error=('abs_error', 'max'), extreme=('extreme', 'sum')).reset_index()
    annual['rmse'] = np.sqrt(annual.pop('mse'))
    peak_rows = frame.loc[group.abs_error.idxmax(), ['ID', 'year', 'FECHA', 'obs', 'timesfm', 'error']]
    annual = annual.merge(peak_rows, on=['ID', 'year'], validate='one_to_one')
    return annual, frame


def main():
    frame = load_pairs(DEFAULT_PALACIOS, DEFAULT_TFM)
    assert not frame.duplicated(['ID', 'FECHA']).any()
    ids = np.sort(frame.ID.unique())
    cells = cell_table(ids, DEFAULT_ZONE, DEFAULT_SUPPORT, DEFAULT_STATIC, DEFAULT_GEO)
    cells = cells[cells.depto != 'fuera_peru'].copy()
    cells['warm'] = cells.zone_label.str.strip().str.endswith("A'")
    frame = frame[frame.ID.isin(cells.ID)].reset_index(drop=True)
    assert np.isfinite(frame[['obs', 'timesfm']].to_numpy()).all()
    abs_error = np.abs(frame.timesfm.to_numpy('float64') - frame.obs.to_numpy('float64'))
    threshold = float(np.quantile(abs_error, .99, method='linear'))
    annual, frame = error_statistics(frame, threshold)
    years = sorted(int(v) for v in frame.year.unique())
    annual = annual.merge(cells[['ID', 'lon', 'lat', 'depto', 'zone_label', 'warm']], on='ID', validate='many_to_one')
    frame = frame.merge(cells[['ID', 'depto', 'zone_label', 'warm']], on='ID', validate='many_to_one')
    OUT.mkdir(parents=True, exist_ok=True)
    annual.to_csv(OUT / 'celda_anio.csv', index=False)
    grouped = frame.groupby('ID', sort=True)
    overall = grouped.agg(n=('error', 'size'), mae=('abs_error', 'mean'), mse=('sq_error', 'mean'),
                          bias=('error', 'mean'), max_error=('abs_error', 'max'), extreme=('extreme', 'sum')).reset_index()
    overall['rmse'] = np.sqrt(overall.pop('mse'))
    assert int(annual.n.sum()) == len(frame)
    assert int(annual.extreme.sum()) == int(frame.extreme.sum())
    assert np.isclose((annual.rmse ** 2 * annual.n).sum(), frame.sq_error.sum())
    rows = []
    annual_index = annual.set_index(['ID', 'year'])
    overall_index = overall.set_index('ID')
    for c in cells.sort_values('ID').itertuples(index=False):
        a = annual_index.loc[c.ID].reindex(years)
        assert a.n.notna().all(), c.ID
        v = overall_index.loc[c.ID]
        peaks = [[pd.Timestamp(r.FECHA).strftime('%Y-%m-%d'), round(float(r.obs), 4),
                  round(float(r.timesfm), 4), round(float(r.error), 4)] for r in a.itertuples()]
        rows.append({'id': int(c.ID), 'lon': round(float(c.lon), 5), 'lat': round(float(c.lat), 5),
                     'depto': str(c.depto), 'zona': str(c.zone_label), 'warm': bool(c.warm),
                     'n': [int(v) for v in a.n], 'extreme': [int(v) for v in a.extreme],
                     **{k: [round(float(v), 5) for v in a[k]] for k in ['max_error', 'rmse', 'mae', 'bias']},
                     'peaks': peaks, 'overall': {k: round(float(v[k]), 5) for k in ['max_error', 'rmse', 'mae', 'bias']}})
    climate = []
    for warm, g in frame.groupby('warm'):
        climate.append({'warm': bool(warm), 'n': len(g), 'cells': int(g.ID.nunique()),
                        'extreme': int(g.extreme.sum()), 'rate1000': float(g.extreme.mean() * 1000),
                        'rmse': float(np.sqrt(g.sq_error.mean())), 'max_error': float(g.abs_error.max())})
    zone = frame.groupby(['zone_label', 'warm'], sort=True).agg(n=('error', 'size'), cells=('ID', 'nunique'),
              extreme=('extreme', 'sum'), max_error=('abs_error', 'max'), mse=('sq_error', 'mean')).reset_index()
    zone['rate1000'] = zone.extreme / zone.n * 1000
    zone['rmse'] = np.sqrt(zone.pop('mse'))
    zone.to_csv(OUT / 'clima.csv', index=False)
    worst = frame.loc[frame.abs_error.idxmax()]
    worst_cell = next(c for c in rows if c['id'] == int(worst.ID))
    top = frame.nlargest(50, 'abs_error')[['ID', 'FECHA', 'depto', 'zone_label', 'warm', 'obs', 'timesfm', 'error', 'abs_error']]
    top.to_csv(OUT / 'episodios_mayor_error.csv', index=False)
    print('UMBRAL P99', threshold, 'MAXIMO', worst[['ID', 'FECHA', 'depto', 'zone_label', 'obs', 'timesfm', 'error']].to_dict(), flush=True)
    print('CLIMAS', json.dumps(climate), flush=True)
    print('ZONAS', zone.nlargest(8, 'rate1000').to_string(index=False), flush=True)
    # Ventana del pico más alto de cada celda: permite inspeccionar el episodio real al seleccionarla.
    peak_idx = grouped.abs_error.idxmax()
    trace_frame = frame.loc[peak_idx, ['ID', 'FECHA']].rename(columns={'FECHA': 'peak_date'})
    trace = frame.merge(trace_frame, on='ID', validate='many_to_one')
    trace = trace[(trace.FECHA - trace.peak_date).dt.days.abs() <= 5]
    traces = {}
    for cid, g in trace.groupby('ID'):
        g = g.sort_values('FECHA')
        traces[int(cid)] = {'start': g.FECHA.iloc[0].strftime('%Y-%m-%d'),
                           'days': (g.FECHA - g.FECHA.iloc[0]).dt.days.tolist(),
                           'obs': g.obs.round(3).tolist(), 'pred': g.timesfm.round(3).tolist()}
    for c in rows:
        c['trace'] = traces[c['id']]
    provenance = {'bead': 'tdew-06n', 'generated_at': datetime.now(timezone.utc).isoformat(),
                  'sources': [str(DEFAULT_PALACIOS), str(DEFAULT_TFM), str(DEFAULT_ZONE), str(DEFAULT_GEO)],
                  'scope': 'Perú; mismos ID y FECHA, con observación y ambas predicciones presentes',
                  'error': 'TimesFM menos Td observada, en grados Celsius; magnitud = valor absoluto',
                  'threshold': threshold, 'quantile': .99, 'inclusive': True,
                  'quantile_method': 'linear', 'peak_fields': ['date', 'obs', 'pred', 'error'],
                  'recurrence': 'Al menos un día con error absoluto >= umbral fijo en ese año',
                  'warm_definition': "Sufijo térmico A': cálido, SENAMHI 2020", 'warm_source': THERMAL_SOURCE,
                  'n': len(frame), 'cells': len(rows),
                  'checks': 'Unicidad ID/FECHA; paridad de conteos, eventos y suma de errores cuadrados entre datos diarios y agregados'}
    payload = {'years': years, 'cells': rows, 'outlines': json.loads(DEFAULT_GEO.read_text()), 'meta': provenance,
               'climate': climate, 'zones': json.loads(zone.to_json(orient='records')), 'worst_id': int(worst.ID)}
    dest = Path('reports/timesfm_benchmark/artifact/datos_errores_celdas.js')
    dest.write_text('window.D_ERRORS=' + json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + ';\n')
    provenance['artifact_sha256'] = hashlib.sha256(dest.read_bytes()).hexdigest()
    (OUT / 'provenance.json').write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    print(f'Listo: {len(rows)} celdas, {len(frame)} pares, {dest.stat().st_size} bytes; peor celda {worst_cell["id"]}', flush=True)


if __name__ == '__main__':
    main()
