/* Sección Paper, KPIs del encabezado y sesgo de Límites: cada cifra procede de las
   filas CSV exportadas en AMENAZAS (datos_amenazas.js) y del cribado de DATOS (datos.js). */
(() => {
  const A = window.AMENAZAS;
  const D = window.DATOS;
  const root = document.getElementById('paper');
  if (!A || !root) return;
  const $ = id => document.getElementById(id);
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const num = (x, sign = false) => x == null ? '—' : (sign && x > 0 ? '+' : '') + Number(x).toFixed(3);
  const miles = n => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  const methods = ['clim','tuned','llr_simple','llr_rezagos_sel','timesfm_anom'];
  const rivals = ['tuned','llr_simple','llr_rezagos_sel'];
  const names = {clim:'Climatología',tuned:'Palacios (tuned)',llr_simple:'LLR simple',llr_rezagos_sel:'LLR con rezagos seleccionado',timesfm_anom:'TimesFM tmin_anom_full'};
  const splits = ['ll4b','ll4'], areas = ['panel','peru'];
  const period = s => A.meta.bloques[s].prueba.join('–');
  const area = a => a === 'panel' ? 'Dominio completo' : 'Perú';
  const columns = splits.flatMap(s => areas.map(a => [s,a]));
  const m = (s,a,k,p='total') => A.porMetodo.find(r => r.split===s && r.ambito===a && r.metodo===k && String(r.periodo)===String(p));
  const gap = (s,a,k,e) => A.brechas.find(r => r.split===s && r.ambito===a && r.metodo_a==='timesfm_anom' && r.metodo_b===k && r.esquema===e);
  const table = (id, heads, rows) => {
    $(id).innerHTML = '<thead><tr>' + heads.map(h=>`<th scope="col">${esc(h)}</th>`).join('') + '</tr></thead><tbody>' + rows.map(r=>'<tr>'+r.map(c=>`<td>${esc(c)}</td>`).join('')+'</tr>').join('')+'</tbody>';
  };
  // Duración legible a partir de segundos de pared.
  const dur = s => {
    if (s == null) return '—';
    if (s >= 72*3600) return `${(s/86400).toFixed(1)} días`;
    if (s >= 3600) { const h = Math.floor(s/3600); return `${h} h ${Math.round((s-h*3600)/60)} min`; }
    if (s >= 60) { const mi = Math.floor(s/60); return `${mi} min ${Math.round(s-mi*60)} s`; }
    return `${Math.round(s)} s`;
  };

  /* ---- precisión ---------------------------------------------------- */
  $('paper-muestra').textContent = areas.map(a => `${area(a)}: ${m('ll4',a,'clim').celdas.toLocaleString('es-PE')} celdas`).join('; ') + '. Mismas filas por columna. Métricas en °C; sesgo = predicción − observación.';
  const renderMetric = key => table('paper-metricas',['Método',...columns.map(([s,a])=>`${period(s)} · ${area(a)}`)], methods.map(k=>[names[k],...columns.map(([s,a])=>num(m(s,a,k)[key],key==='sesgo'))]));
  renderMetric('rmse');
  root.querySelectorAll('[data-paper-metric]').forEach(b=>b.addEventListener('click',()=>{
    root.querySelectorAll('[data-paper-metric]').forEach(x=>x.setAttribute('aria-selected',String(x===b)));
    renderMetric(b.dataset.paperMetric);
  }));
  const interval = r => `[${num(r.ic_lo,true)}; ${num(r.ic_hi,true)}]`;
  table('paper-brechas',['Período','Ámbito','Rival','ΔRMSE','IC espacial 2°','IC mes-año'],columns.flatMap(([s,a])=>rivals.map(k=>{
    const space = gap(s,a,k,'espacial_2g'), time = gap(s,a,k,'mes_anio');
    return [period(s),area(a),names[k],num(time.brecha,true),interval(space),interval(time)];
  })));
  const esquemaN = {espacial_2g:'espacial', mes_anio:'mes-año'};
  const conCero = columns.flatMap(([s,a]) => rivals.flatMap(k => ['espacial_2g','mes_anio'].filter(e => { const r = gap(s,a,k,e); return r.ic_lo <= 0 && r.ic_hi >= 0; }).map(e => `frente al ${names[k].replace('Palacios (tuned)','método de Palacios')} en ${a === 'panel' ? 'el dominio completo' : 'el Perú'}, ${period(s)} (IC ${esquemaN[e]})`)));
  $('paper-ic').textContent = `${miles(A.meta.bootstrap)} réplicas por esquema. Frente a los LLR las brechas son menores que frente a Palacios. ` +
    (conCero.length ? `El IC incluye el cero ${conCero.join('; ')}: con este análisis no se distinguió una diferencia en esos casos. ` : '') +
    'Los dos remuestreos son separados y ninguno cubre a la vez la dependencia espacial y la temporal. Un IC que contiene cero no demuestra equivalencia.';
  const renderZones = (s,a) => {
    const rows = A.porZona.filter(r=>r.split===s&&r.ambito===a&&r.metodo==='timesfm_anom');
    table('paper-zonas',['Zona','Celdas','RMSE TimesFM',...rivals.map(k=>`Δ vs ${names[k]}`)],rows.map(r=>[r.zone_label,r.celdas,num(r.rmse),...rivals.map(k=>{
      const b=A.porZona.find(x=>x.split===s&&x.ambito===a&&x.zone_id===r.zone_id&&x.metodo===k);
      return b ? num(r.rmse-b.rmse,true) : 'sin dato';
    })]));
  };
  columns.forEach(([s,a],i)=>{
    const b=document.createElement('button'); b.type='button';b.setAttribute('role','tab');b.setAttribute('aria-selected',String(i===0));b.textContent=`${period(s)} · ${area(a)}`;
    b.addEventListener('click',()=>{ $('paper-zona-tabs').querySelectorAll('button').forEach(x=>x.setAttribute('aria-selected',String(x===b)));renderZones(s,a); });
    $('paper-zona-tabs').append(b);
  });
  renderZones(...columns[0]);

  /* ---- robustez: cribado de configuraciones -------------------------- */
  const DESC = {
    'tmin_anom_full':'Td y Tmin en anomalía · contexto desde 1981 (elegida)',
    'tmin_doy_td_full':'Td y Tmin crudas más día del año · desde 1981',
    'tmin_td_symavg':'Td y Tmin crudas, promediado simétrico · desde 1981',
    'tmin_td_znorm':'Td y Tmin crudas, normalización z externa · desde 1981',
    'tmin_td_full':'Td y Tmin crudas · desde 1981',
    'tmin_td_med':'Td y Tmin crudas · desde 2002 (11 años)',
    'tmin_td_short':'Td y Tmin crudas · desde 2011 (2 años)',
    'uni_anom_full':'solo Td en anomalía, sin Tmin · desde 1981',
    'uni_td_full':'solo Td cruda, sin Tmin · desde 1981'
  };
  const cribado = D && D.tablas && D.tablas.cribado ? D.tablas.cribado : [];
  const tunedC = cribado.find(r => r.method === 'tuned');
  const variantes = cribado.filter(r => r.method.startsWith('timesfm:'));
  const ganan = variantes.filter(r => tunedC && r.rmse < tunedC.rmse);
  const pierden = variantes.filter(r => tunedC && r.rmse >= tunedC.rmse);
  const clave = r => r.method.replace('timesfm:','');
  if (tunedC) {
    $('kpi-cribado').textContent = `${ganan.length} de ${variantes.length}`;
    $('paper-robustez-titulo').textContent = `${ganan.length} de las ${variantes.length} configuraciones de TimesFM superan a Palacios`;
    $('paper-cribado-sub').textContent = `Cribado sobre ${miles(tunedC.cells)} celdas del bloque ${period('ll4')}. RMSE en °C; menor es mejor. Sin IC: es la etapa en que se eligió la configuración.`;
    const filas = cribado.filter(r => r.method.startsWith('timesfm:') || r.method === 'tuned' || r.method === 'climatology');
    table('paper-cribado',['Configuración','Entradas y contexto','RMSE','Δ vs Palacios'],filas.map(r => r.method === 'tuned'
      ? ['Palacios (tuned)','recetas por zona × día del año',num(r.rmse),'—']
      : r.method === 'climatology'
        ? ['Climatología','media por celda y día del año',num(r.rmse),num(r.rmse - tunedC.rmse,true)]
        : [clave(r), DESC[clave(r)] || '', num(r.rmse), num(r.rmse - tunedC.rmse,true)]));
    const crudaB = areas.map(a => `${num(m('ll4b',a,'timesfm_td').rmse)} frente a ${num(m('ll4b',a,'tuned').rmse)} °C en ${a === 'panel' ? 'el dominio completo' : 'el Perú'}`);
    const crudaGana = areas.every(a => m('ll4b',a,'timesfm_td').rmse < m('ll4b',a,'tuned').rmse);
    const med = cribado.find(r => r.method === 'timesfm:tmin_td_med');
    $('paper-robustez-nota').textContent = `No superan a Palacios: ${pierden.map(r => `${clave(r)} (${DESC[clave(r)] || ''})`).join('; ')}. ` +
      'De ahí las condiciones de uso: TimesFM necesita la Tmin del período y un historial local largo' +
      (med && med.rmse < tunedC.rmse ? '; con 11 años de contexto ya supera a Palacios. ' : '. ') +
      (crudaGana ? `Frente a Palacios, la ventaja tampoco depende de trabajar en anomalías: en ${period('ll4b')}, fuera del cribado, la configuración con Td y Tmin crudas (tmin_td_full) obtiene ${crudaB.join(' y ')}.` : '');
  }

  /* ---- requisitos de diseño ------------------------------------------ */
  const requirements = {
    clim:['ninguna','ninguna','media de Td por celda y día del año','CPU'],
    llr_simple:['ninguna',`ventana h global en una grilla de 7 valores, con los últimos ${A.meta.aniosValidacion} años de entrenamiento`,'coeficientes por celda','CPU'],
    llr_rezagos_sel:['ninguna',`ventana h y año de inicio por validación interna; rezagos de Tmin de ${A.meta.rezagos.join(', ')} días`,'coeficientes por celda','CPU'],
    tuned:['shapefile SENAMHI de 41 zonas climáticas','receta y h por zona × día del año, con un pool de 11 términos candidatos','coeficientes por celda; predicción autorregresiva con sus rezagos de Td','GPU (CuPy)'],
    timesfm_anom:['ninguna fuera de los datos de cada celda','una configuración entre 9, elegida una vez','ninguno: checkpoint preentrenado de 330M parámetros','GPU']
  };
  table('paper-requisitos',['Método','Información del país','Búsqueda previa','Ajuste','Hardware'],methods.map(k=>[names[k],...requirements[k]]));

  /* ---- costo: entrenamiento, inferencia y total ---------------------- */
  const c = (metodo,bloque,etapa) => A.costo.find(r => r.metodo===metodo && r.bloque===bloque && r.etapa===etapa);
  const seg = r => r ? Number(r.segundos_pared) : null;
  const suma = (...xs) => xs.some(x => x == null) ? null : xs.reduce((p,q)=>p+q,0);
  const backtest = b => {
    const sel = seg(c('tuned',b,'seleccion de recetas (solo anios de entrenamiento)'));
    const ajp = seg(c('tuned',b,'ajuste + prediccion (backtest)'));
    const tf = seg(c('timesfm_anom',b,'prediccion (sin ajuste ni seleccion)'));
    return {sel, ajp, tf, tunedTotal: suma(sel,ajp), tfTotal: tf};
  };
  const bB = backtest('ll4b'), bA = backtest('ll4');
  const pSel = c('tuned','produccion 1981-2016','seleccion de recetas (grid completo)');
  const pAj = c('tuned','produccion 1981-2016','ajuste (grid completo)');
  const pPred = c('tuned','real 2017-2020','prediccion (grid completo)');
  const pTf = c('timesfm_anom','real 2017-2020','prediccion producto completo');
  const prod = {sel: seg(pSel), aj: seg(pAj), pred: seg(pPred), tf: seg(pTf)};
  prod.tunedTotal = suma(prod.sel, prod.aj, prod.pred);
  const escB = `Bloque ${period('ll4b')}, misma máquina`;
  const escA = `Bloque ${period('ll4')}`;
  const escP = `Producto: entrenamiento 1981–2016 (${miles(pSel.celdas)} celdas) y reconstrucción 2017–2020 (${miles(pTf.celdas)} celdas)`;
  table('paper-costos',['Escala','Método','Selección de recetas','Ajuste','Predicción','Total'],[
    [escB,'Palacios (tuned)',dur(bB.sel),`${dur(bB.ajp)} (con predicción)`,'incluida en ajuste',dur(bB.tunedTotal)],
    [escB,'TimesFM','no aplica','no aplica',dur(bB.tf),dur(bB.tfTotal)],
    [escA,'Palacios (tuned)',dur(bA.sel),`${dur(bA.ajp)} (con predicción)`,'incluida en ajuste',dur(bA.tunedTotal)],
    [escA,'TimesFM','no aplica','no aplica',dur(bA.tf),dur(bA.tfTotal)],
    [escP,'Palacios (tuned)',dur(prod.sel),dur(prod.aj),dur(prod.pred),dur(prod.tunedTotal)],
    [escP,'TimesFM','no aplica','no aplica',dur(prod.tf),dur(prod.tf)]
  ]);
  const cr = c('timesfm (9 variantes)','ll4','seleccion de variante (cribado)');
  const entrena = suma(prod.sel, prod.aj);
  const lecturaProd = prod.tf > prod.tunedTotal
    ? `A escala de producto, TimesFM se ahorra ${dur(entrena)} de selección y ajuste, pero su predicción (${dur(prod.tf)}) supera el total de Palacios; ya entrenado, Palacios reconstruye 2017–2020 en ${dur(prod.pred)}.`
    : `A escala de producto, TimesFM se ahorra ${dur(entrena)} de selección y ajuste y su predicción toma ${dur(prod.tf)}.`;
  $('paper-costo-nota').textContent = `En el bloque ${period('ll4b')}, en la misma máquina, el total es ${dur(bB.tunedTotal)} para Palacios y ${dur(bB.tfTotal)} para TimesFM: del mismo orden. ${lecturaProd} ` +
    'El argumento a favor de TimesFM está en que no requiere diseño ni entrenamiento; en cómputo total no sale más barato. ' +
    (cr ? `La configuración de TimesFM se eligió una sola vez, en un cribado de 9 configuraciones sobre ${miles(cr.celdas)} celdas, de las que se puntúan ${miles(tunedC ? tunedC.cells : 0)} (${dur(seg(cr))}), y se reutilizó sin cambios en ${period('ll4b')}. ` : '') +
    'Las corridas de producto no forman una comparación controlada: los registros de Palacios no anotan el host y TimesFM compartió la GPU en algunos tramos. El preprocesamiento de PISCO, el regrillado de Tmin y las climatologías son comunes a todos los métodos y no se cargan a ninguno. Los tiempos de los LLR seleccionados no se midieron.';
  $('kpi-entrena-sub').textContent = `Palacios: ${dur(entrena)} de selección de recetas y ajuste en producción`;

  /* ---- elección y KPIs -------------------------------------------------- */
  const gains = columns.map(([s,a]) => m(s,a,'tuned').rmse - m(s,a,'timesfm_anom').rmse);
  $('paper-eleccion-timesfm').textContent = 'Menos RMSE que Palacios: ' + columns.map(([s,a],i)=>`${num(gains[i])} °C en ${period(s)}, ${a === 'panel' ? 'dominio completo' : 'Perú'}`).join('; ') + '.';
  $('paper-eleccion-tuned').textContent = `Una vez seleccionadas las recetas y ajustados los coeficientes, Palacios reconstruye 2017–2020 en ${dur(prod.pred)}, frente a ${dur(prod.tf)} de TimesFM.`;
  const brTuned = columns.flatMap(([s,a]) => ['espacial_2g','mes_anio'].map(e => gap(s,a,'tuned',e)));
  $('kpi-brecha').textContent = `${num(Math.min(...gains))}–${num(Math.max(...gains))} °C`;
  $('kpi-brecha-sub').textContent = 'en los dos bloques, en el Perú y en el dominio completo' + (brTuned.every(r => r.ic_hi < 0) ? '; IC del 95 % sin cero en los dos esquemas' : '');

  /* ---- sesgo en Límites ------------------------------------------------ */
  const sg = (s,k) => num(m(s,'panel',k).sesgo,true);
  $('lim-sesgo').textContent = `En el dominio completo, el sesgo de TimesFM es ${sg('ll4b','timesfm_anom')} °C en ${period('ll4b')} y ${sg('ll4','timesfm_anom')} °C en ${period('ll4')}; el de Palacios, ${sg('ll4b','tuned')} y ${sg('ll4','tuned')} °C. La tabla de precisión de la sección Paper lo muestra también para el Perú.`;
})();
