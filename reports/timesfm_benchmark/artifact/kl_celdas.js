/* Ubicación → repetición → detalle. Guías MIT GTL, sesiones 4, 5 y 6. */
(() => {
  const K = window.D_KLC_CELLS, root = document.getElementById('kl-celdas');
  if (!root) return;
  if (!K) { root.textContent = 'No se cargaron los datos por celda.'; return; }
  const $ = id => document.getElementById(id);
  const fmt = n => n.toLocaleString('es-PE');
  const names = {timesfm: 'TimesFM', llr: 'Palacios'};
  const ink = '#086c67', transient = '#c2a16c', neutral = '#bdc8cc';
  let model = 'timesfm', period = 'repeat', selected = null, annualRegion = 'loreto';
  let zoom = 1, center = null;
  const valid = c => c.n.filter(n => n > 0).length;
  const repeat = (c, m = model) => c.n.reduce((s, n, y) => s + (n > 0 && c[m][y] < c.obs[y] ? 1 : 0), 0);
  const diff = (c, y) => c.n[y] ? 100 * (c[model][y] - c.obs[y]) / c.n[y] : null;
  const allDiff = c => 100 * (c[model].reduce((a, b) => a + b, 0) - c.obs.reduce((a, b) => a + b, 0)) / c.n.reduce((a, b) => a + b, 0);
  const cellsPeru = K.cells.filter(c => c.depto !== 'fuera_peru');
  const scope = () => cellsPeru;
  const label = c => c.depto.toLocaleLowerCase('es').replace(/(^|\s)\S/g, s => s.toLocaleUpperCase('es'));
  const polygons = f => f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
  function extent(features, padding = .35) {
    const points = features.flatMap(f => polygons(f).flatMap(p => p.flat()));
    return [Math.min(...points.map(p => p[0])) - padding, Math.max(...points.map(p => p[0])) + padding,
            Math.min(...points.map(p => p[1])) - padding, Math.max(...points.map(p => p[1])) + padding];
  }
  const loreto = K.outlines.features.filter(f => f.properties.NOMBDEP === 'LORETO');
  const countryBounds = extent(K.outlines.features), loretoBounds = extent(loreto);
  function frame(canvas) {
    const main = canvas.id === 'kc-map';
    const local = canvas.id === 'kc-inset' || (!main && annualRegion === 'loreto');
    const bounds = local ? loretoBounds : countryBounds;
    const z = main ? zoom : 1, mid = main && center ? center : [(bounds[0] + bounds[1]) / 2, (bounds[2] + bounds[3]) / 2];
    const dx = (bounds[1] - bounds[0]) / z, dy = (bounds[3] - bounds[2]) / z;
    return {bounds, main, local, mid, dx, dy, xy: (lon, lat) => [(lon - mid[0] + dx / 2) / dx * canvas.width, (mid[1] + dy / 2 - lat) / dy * canvas.height]};
  }
  function isInside(c, f) { return c.lon >= f.mid[0] - f.dx / 2 && c.lon <= f.mid[0] + f.dx / 2 && c.lat >= f.mid[1] - f.dy / 2 && c.lat <= f.mid[1] + f.dy / 2; }
  function category(c, mode) {
    if (mode === 'repeat') { const n = repeat(c); return n === 4 ? 2 : n > 0 ? 1 : 0; }
    const d = mode === 'all' ? allDiff(c) : diff(c, Number(mode));
    return d !== null && d < 0 ? 2 : 0;
  }
  function draw(canvas, mode) {
    const f = frame(canvas);
    canvas.width = 900; canvas.height = Math.round(900 * (f.bounds[3] - f.bounds[2]) / (f.bounds[1] - f.bounds[0]));
    const ctx = canvas.getContext('2d'), xy = f.xy, scale = 900 / (canvas.getBoundingClientRect().width || 400);
    const markerScale = Math.min(1, Math.max(.5, (canvas.getBoundingClientRect().width || 400) / 350));
    ctx.fillStyle = '#f8fafb'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    function outline(feature, highlight = false) {
      ctx.fillStyle = highlight ? '#f4f8f6' : '#fff'; ctx.strokeStyle = highlight ? '#668d86' : '#d2dce0'; ctx.lineWidth = (highlight ? .9 : .55) * scale;
      for (const poly of polygons(feature)) {
        ctx.beginPath();
        for (const ring of poly) { ring.forEach(([lon, lat], i) => { const [x, y] = xy(lon, lat); i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); }
        ctx.fill('evenodd'); ctx.stroke();
      }
    }
    K.outlines.features.forEach(feature => outline(feature, feature.properties.NOMBDEP === 'LORETO'));
    // Primero el contexto, después las celdas de interés para que no queden tapadas.
    const cells = scope().filter(c => (!f.local || c.depto === 'LORETO') && isInside(c, f));
    for (const group of [0, 1, 2]) for (const c of cells) {
      if (category(c, mode) !== group) continue;
      const [x, y] = xy(c.lon, c.lat), r = (group === 2 ? 1.65 : group === 1 ? 1.3 : .85) * markerScale * scale;
      ctx.fillStyle = group === 2 ? ink : group === 1 ? transient : neutral;
      if (group === 2) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); }
      else ctx.fillRect(x - r, y - r, r * 2, r * 2);
    }
    if (f.main && zoom === 1) {
      // Punto interior calculado con representative_point() sobre el GeoJSON de Loreto.
      const [ax, ay] = xy(-74.39464983316569, -4.38537253521345), tx = ax + 48 * scale, ty = ay - 37 * scale;
      ctx.strokeStyle = ink; ctx.lineWidth = 1 * scale;
      ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(tx - 7 * scale, ty + 5 * scale); ctx.stroke();
      ctx.font = `600 ${12 * scale}px sans-serif`; ctx.lineWidth = 5 * scale; ctx.strokeStyle = '#fff'; ctx.strokeText('LORETO', tx, ty); ctx.fillStyle = ink; ctx.fillText('LORETO', tx, ty);
      ctx.fillStyle = '#667985'; ctx.font = `${11 * scale}px sans-serif`; ctx.fillText('N ↑', 14 * scale, 24 * scale);
    }
    if (selected && isInside(selected, f) && (!f.local || selected.depto === 'LORETO')) {
      const [x, y] = xy(selected.lon, selected.lat);
      ctx.beginPath(); ctx.arc(x, y, 6 * scale, 0, Math.PI * 2); ctx.strokeStyle = '#fff'; ctx.lineWidth = 4 * scale; ctx.stroke();
      ctx.strokeStyle = '#17212a'; ctx.lineWidth = 1.5 * scale; ctx.stroke();
    }
    canvas.setAttribute('aria-label', `${f.local ? 'Loreto ampliado' : 'Perú'} · ${names[model]} · ${mode === 'repeat' ? 'celdas donde se repite los cuatro años' : mode === 'all' ? '2013–2016 agrupados' : K.years[Number(mode)]}. Al seleccionar un punto se muestran su ID y coordenadas.`);
  }
  function annualCells() { return annualRegion === 'loreto' ? scope().filter(c => c.depto === 'LORETO') : scope(); }
  function maps() {
    draw($('kc-map'), period); draw($('kc-inset'), period);
    K.years.forEach((y, i) => draw($('kc-year-' + y), String(i)));
  }
  function choose(c, focus = false) {
    selected = c;
    if (focus) { center = [c.lon, c.lat]; zoom = 4; }
    const rows = K.years.map((y, i) => `<tr><td>${y}</td><td>${fmt(c.n[i])}</td><td>${fmt(c.obs[i])}</td><td>${fmt(c.timesfm[i])}</td><td>${fmt(c.llr[i])}</td></tr>`).join('');
    $('kc-detail').innerHTML = `<h3>Celda ${c.id} · ${label(c)}</h3><p>Longitud ${c.lon.toFixed(4)}° · latitud ${c.lat.toFixed(4)}°<br>Zona climática ${c.zona}</p><div class="tabla-caja"><table><caption>Días con valores entre 20 y menos de 24 °C</caption><thead><tr><th>Año</th><th>Evaluados</th><th>Observados</th><th>TimesFM</th><th>Palacios</th></tr></thead><tbody>${rows}</tbody></table></div><p>En ${repeat(c)} de ${valid(c)} años, ${names[model]} estima menos valores en ese intervalo. El círculo identifica esta misma celda en los mapas donde está dentro de la extensión mostrada.</p>`;
    $('kc-cell-details').open = true;
    maps();
    if (focus) $('kc-cell-details').scrollIntoView({block: 'center'});
  }
  function updateAnnual() {
    const cells = annualCells(), repeated = cells.filter(c => valid(c) === 4 && repeat(c) === 4).length;
    $('kc-years-title').textContent = annualRegion === 'loreto' ? 'En Loreto, la diferencia aparece cada año' : 'Las mismas celdas, comparadas año por año';
    K.years.forEach((y, i) => { $('kc-year-note-' + y).textContent = `${fmt(cells.filter(c => c.n[i] && c[model][i] < c.obs[i]).length)} celdas con la diferencia`; });
    $('kc-persistence-note').innerHTML = `<strong>${fmt(repeated)} de las mismas celdas ${annualRegion === 'loreto' ? 'de Loreto ' : ''}presentan la diferencia en los cuatro años.</strong> Se evaluaron ${fmt(cells.length)} celdas en esta extensión con ${names[model]}. Las restantes pueden presentarla en menos años o en ninguno.`;
  }
  function render() {
    const cells = scope();
    $('kc-headline').textContent = 'En Loreto se concentra la diferencia que se repite los cuatro años';
    $('kc-scope').textContent = `${fmt(cells.length)} celdas evaluadas en Perú · 2013–2016`;
    $('kc-summary').innerHTML = Object.keys(names).map(m => {
      const all = cells.filter(c => valid(c) === 4 && repeat(c, m) === 4), inLoreto = all.filter(c => c.depto === 'LORETO').length;
      const fraction = all.length ? 100 * inLoreto / all.length : 0;
      return `<div class="kc-result ${m === model ? 'is-active' : ''}"><h3>${names[m]}</h3><strong>${fmt(all.length)}</strong><span class="kc-count-unit">celdas · los mismos 4 años</span><p><b>${fmt(inLoreto)} en Loreto (${fraction.toFixed(0)} %)</b> · ${fmt(all.length - inLoreto)} en el resto del Perú</p><div class="kc-part" role="img" aria-label="Loreto ${inLoreto} de ${all.length} celdas"><i style="width:${fraction}%"></i></div></div>`;
    }).join('');
    $('kc-map-title').textContent = period === 'repeat' ? `La diferencia se repite sobre todo en Loreto · ${names[model]}` : `Celdas con la diferencia · ${names[model]} · ${period === 'all' ? '2013–2016 agrupados' : K.years[Number(period)]}`;
    $('kc-map-sub').textContent = period === 'repeat' ? 'Los puntos oscuros permiten ubicar los lugares donde la diferencia aparece en cada año de 2013–2016.' : 'El color oscuro identifica las celdas con menos valores entre 20 y 24 °C que los observados en el período seleccionado.';
    $('kc-inset-title').textContent = period === 'repeat' ? `${fmt(cells.filter(c => c.depto === 'LORETO' && repeat(c) === 4).length)} celdas se repiten los cuatro años` : `El mismo período, ampliado en Loreto`;
    $('kc-legend').innerHTML = period === 'repeat'
      ? `<span><i style="background:${ink};border-radius:50%"></i>Los 4 años</span><span><i style="background:${transient}"></i>Entre 1 y 3 años</span><span><i style="background:${neutral}"></i>Ningún año</span>`
      : `<span><i style="background:${ink};border-radius:50%"></i>Menos valores en el intervalo</span><span><i style="background:${neutral}"></i>Igual o más</span>`;
    $('kc-period').value = period;
    updateAnnual(); maps();
    if (selected) choose(selected);
  }
  function nearest(event, canvas) {
    const rect = canvas.getBoundingClientRect(), x = (event.clientX - rect.left) * canvas.width / rect.width,
          y = (event.clientY - rect.top) * canvas.height / rect.height, f = frame(canvas);
    let best = null, distance = Infinity;
    for (const c of scope()) { if ((f.local && c.depto !== 'LORETO') || !isInside(c, f)) continue; const [cx, cy] = f.xy(c.lon, c.lat), d = Math.hypot(cx - x, cy - y); if (d < distance) { distance = d; best = c; } }
    return best && distance < 9 * canvas.width / rect.width ? best : null;
  }
  let drag = null, suppressClick = false;
  $('kc-map').addEventListener('pointerdown', e => {
    if (e.pointerType === 'touch') return;
    const f = frame($('kc-map'));
    drag = {x: e.clientX, y: e.clientY, mid: [...f.mid], dx: f.dx, dy: f.dy}; suppressClick = false;
    $('kc-map').setPointerCapture(e.pointerId);
  });
  $('kc-map').addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (Math.hypot(dx, dy) < 5 && !suppressClick) return;
    suppressClick = true;
    const rect = $('kc-map').getBoundingClientRect();
    center = [drag.mid[0] - dx / rect.width * drag.dx, drag.mid[1] + dy / rect.height * drag.dy];
    draw($('kc-map'), period);
  });
  $('kc-map').addEventListener('pointerup', () => { drag = null; });
  $('kc-map').addEventListener('pointercancel', () => { drag = null; suppressClick = false; });
  for (const id of ['kc-map', 'kc-inset', ...K.years.map(y => 'kc-year-' + y)]) $(id).addEventListener('click', e => {
    if (id === 'kc-map' && suppressClick) { suppressClick = false; return; }
    const c = nearest(e, $(id)); if (!c) return;
    if (id.startsWith('kc-year-')) { period = String(K.years.indexOf(Number(id.slice(8)))); render(); }
    choose(c);
  });
  $('kc-model').addEventListener('change', e => { model = e.target.value; render(); });
  $('kc-period').addEventListener('change', e => { period = e.target.value; render(); });
  $('kc-year-region').addEventListener('change', e => { annualRegion = e.target.value; updateAnnual(); maps(); });
  $('kc-zoom-in').addEventListener('click', () => { if (selected) center = [selected.lon, selected.lat]; zoom = Math.min(12, zoom * 1.6); maps(); });
  $('kc-zoom-out').addEventListener('click', () => { zoom = Math.max(1, zoom / 1.6); if (zoom === 1) center = null; maps(); });
  $('kc-reset').addEventListener('click', () => { zoom = 1; center = null; maps(); });
  new ResizeObserver(() => maps()).observe($('kc-map').parentElement);
  render();
})();
