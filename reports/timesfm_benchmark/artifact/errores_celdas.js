/* Error pareado en °C. Un pico conserva la misma celda, fecha, observación y predicción. */
(() => {
  const K = window.D_ERRORS, root = document.getElementById('kl-celdas');
  if (!root) return;
  if (!K) { root.textContent = 'No se cargaron los errores por celda.'; return; }
  const $ = id => document.getElementById(id), fmt = n => n.toLocaleString('es-PE');
  const f = (n, d = 2) => n.toLocaleString('es-PE', {minimumFractionDigits:d, maximumFractionDigits:d});
  const signed = n => (n > 0 ? '+' : '') + f(n);
  const title = text => text.toLocaleLowerCase('es').replace(/(^|\s)\S/g, s => s.toLocaleUpperCase('es'));
  const date = text => new Date(text + 'T00:00:00Z').toLocaleDateString('es-PE', {day:'numeric',month:'short',year:'numeric',timeZone:'UTC'});
  const colors = ['#c9d2d7','#d3b886','#c88543','#aa512e','#762f23'];
  const threshold = K.meta.threshold, cells = K.cells.filter(c => c.depto !== 'fuera_peru');
  let period = 'max', climate = 'all', annualRegion = 'focus', zoom = 1, center = null;
  let selected = cells.find(c => c.id === K.worst_id);
  const scope = () => cells.filter(c => climate === 'all' || c.warm === (climate === 'warm'));
  const repeat = c => c.extreme.filter(n => n > 0).length;
  const peakYear = c => c.max_error.indexOf(Math.max(...c.max_error));
  const value = (c, mode = period) => mode === 'repeat' ? repeat(c) : mode === 'max' ? c.overall.max_error : c.max_error[Number(mode)];
  const peak = (c, i) => {const [day,obs,pred,error] = c.peaks[i]; return {day,obs,pred,error};};
  const polygons = feat => feat.geometry.type === 'Polygon' ? [feat.geometry.coordinates] : feat.geometry.coordinates;
  function extent(features) {
    const pts = features.flatMap(feat => polygons(feat).flatMap(p => p.flat()));
    return [Math.min(...pts.map(p=>p[0]))-.35, Math.max(...pts.map(p=>p[0]))+.35,
            Math.min(...pts.map(p=>p[1]))-.35, Math.max(...pts.map(p=>p[1]))+.35];
  }
  const countryBounds = extent(K.outlines.features);
  function frame(canvas) {
    const main = canvas.id === 'kc-map', local = canvas.id === 'kc-inset' || (!main && annualRegion === 'focus');
    const features = K.outlines.features.filter(feat => feat.properties.NOMBDEP === selected.depto);
    const bounds = local ? extent(features) : countryBounds, z = main ? zoom : 1;
    const mid = main && center ? center : [(bounds[0]+bounds[1])/2,(bounds[2]+bounds[3])/2];
    const dx=(bounds[1]-bounds[0])/z,dy=(bounds[3]-bounds[2])/z;
    return {main,local,bounds,mid,dx,dy,xy:(lon,lat)=>[(lon-mid[0]+dx/2)/dx*canvas.width,(mid[1]+dy/2-lat)/dy*canvas.height]};
  }
  const inside = (c,v) => c.lon >= v.mid[0]-v.dx/2 && c.lon <= v.mid[0]+v.dx/2 && c.lat >= v.mid[1]-v.dy/2 && c.lat <= v.mid[1]+v.dy/2;
  const category = (c,mode) => mode === 'repeat' ? repeat(c) : Math.min(4,Math.floor(value(c,mode)/2));
  function draw(canvas,mode) {
    const v=frame(canvas);canvas.width=900;canvas.height=Math.round(900*(v.bounds[3]-v.bounds[2])/(v.bounds[1]-v.bounds[0]));
    const ctx=canvas.getContext('2d'),scale=900/(canvas.getBoundingClientRect().width||400),rScale=Math.min(1,Math.max(.5,(canvas.getBoundingClientRect().width||400)/350));
    ctx.fillStyle='#f8fafb';ctx.fillRect(0,0,canvas.width,canvas.height);
    for(const feat of K.outlines.features){
      const focus=feat.properties.NOMBDEP===selected.depto;ctx.fillStyle=focus?'#fbf7f1':'#fff';ctx.strokeStyle=focus?'#b4a18e':'#d2dce0';ctx.lineWidth=(focus?.9:.55)*scale;
      for(const poly of polygons(feat)){ctx.beginPath();for(const ring of poly){ring.forEach(([lon,lat],i)=>{const[x,y]=v.xy(lon,lat);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.closePath()}ctx.fill('evenodd');ctx.stroke()}
    }
    const visible=scope().filter(c=>(!v.local||c.depto===selected.depto)&&inside(c,v));
    for(let group=0;group<5;group++)for(const c of visible){
      if(category(c,mode)!==group)continue;const[x,y]=v.xy(c.lon,c.lat),r=(group>1?1.65:1)*rScale*scale;
      ctx.fillStyle=colors[group];ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();
    }
    if(inside(selected,v)){
      const[x,y]=v.xy(selected.lon,selected.lat);ctx.beginPath();ctx.arc(x,y,6*scale,0,Math.PI*2);ctx.strokeStyle='#fff';ctx.lineWidth=4*scale;ctx.stroke();ctx.strokeStyle='#17212a';ctx.lineWidth=1.5*scale;ctx.stroke();
      if(v.main&&zoom===1){const text=title(selected.depto),tx=Math.min(canvas.width-(text.length*7+10)*scale,x+25*scale),ty=Math.max(35*scale,y-25*scale);ctx.beginPath();ctx.moveTo(x,y-6*scale);ctx.lineTo(tx,ty+5*scale);ctx.lineWidth=scale;ctx.strokeStyle='#762f23';ctx.stroke();ctx.font=`600 ${12*scale}px sans-serif`;ctx.lineWidth=5*scale;ctx.strokeStyle='#fff';ctx.strokeText(text,tx,ty);ctx.fillStyle='#762f23';ctx.fillText(text,tx,ty)}
    }
    if(v.main){ctx.fillStyle='#667985';ctx.font=`${11*scale}px sans-serif`;ctx.fillText('N ↑',14*scale,24*scale)}
    canvas.setAttribute('aria-label',`${v.local?title(selected.depto):'Perú'} · TimesFM · ${mode==='repeat'?'años con errores grandes':mode==='max'?'mayor error diario de 2013–2016, en grados Celsius':'mayor error diario de '+K.years[Number(mode)]+', en grados Celsius'}. Se puede seleccionar una celda.`);
  }
  const legend = () => colors.map((color,i)=>`<span><i style="background:${color}"></i>${['Menos de 2 °C','2–4 °C','4–6 °C','6–8 °C','8 °C o más'][i]}</span>`).join('');
  function trace(c){
    const t=c.trace, W=420,H=210,L=40,R=12,T=18,B=38;
    let low=Math.floor(Math.min(...t.obs,...t.pred)),high=Math.ceil(Math.max(...t.obs,...t.pred));if(low===high)high++;
    const X=i=>L+i/(t.days.length-1)*(W-L-R),Y=n=>T+(high-n)/(high-low)*(H-T-B);
    let out='';for(let i=0;i<4;i++){const n=low+(high-low)*i/3,y=Y(n);out+=`<line x1="${L}" x2="${W-R}" y1="${y}" y2="${y}" stroke="var(--line-soft)"/><text x="${L-5}" y="${y+4}" text-anchor="end" font-size="11" fill="var(--ink-soft)">${f(n,1)}</text>`}
    for(const [key,col]of[['obs','var(--ink)'],['pred','#aa512e']]){
      out+=`<path d="${t[key].map((n,i)=>(i?'L':'M')+X(i)+','+Y(n)).join(' ')}" fill="none" stroke="${col}" stroke-width="2"/>`;
      t[key].forEach((n,i)=>{out+=`<circle cx="${X(i)}" cy="${Y(n)}" r="2" fill="${col}"/>`});
    }
    for(const i of[0,Math.floor(t.days.length/2),t.days.length-1]){const day=new Date(new Date(t.start+'T00:00:00Z').getTime()+t.days[i]*86400000).toISOString().slice(0,10);out+=`<text x="${X(i)}" y="${H-12}" text-anchor="middle" font-size="10" fill="var(--ink-soft)">${day.slice(5)}</text>`}
    return `<p class="kc-event">Ventana alrededor del mayor pico de esta celda. Eje vertical: Td en °C.</p><svg class="kc-trace" viewBox="0 0 ${W} ${H}" role="img" aria-label="Td observada y TimesFM durante los días próximos al mayor error">${out}</svg><div class="leyenda-linea"><span><i style="background:var(--ink)"></i>Td observada</span><span><i style="background:#aa512e"></i>TimesFM</span></div>`;
  }
  function detail(){
    const c=selected,i=period==='max'||period==='repeat'?peakYear(c):Number(period),p=peak(c,i);
    const rows=K.years.map((year,j)=>{const q=peak(c,j);return `<tr${i===j?' class="foco"':''}><td>${q.day}</td><td>${f(q.obs)}</td><td>${f(q.pred)}</td><td>${signed(q.error)}</td><td>${c.extreme[j]} / ${c.n[j]}</td></tr>`}).join('');
    $('kc-detail').innerHTML=`<h3>Celda ${c.id} · ${title(c.depto)}</h3><p>Longitud ${c.lon.toFixed(4)}° · latitud ${c.lat.toFixed(4)}°<br>Clima ${c.warm?'cálido':thermal(c.zona)} · ${c.zona}</p><p class="kc-event"><strong>${date(p.day)}: error de ${f(Math.abs(p.error))} °C.</strong><br>Se observó ${f(p.obs)} °C y TimesFM estimó ${f(p.pred)} °C (${p.error<0?'por debajo':'por encima'} de lo observado).</p>${i===peakYear(c)?trace(c):''}<div class="tabla-caja"><table><caption>El peor día de cada año · Td y error en °C</caption><thead><tr><th>Fecha</th><th>Td obs.</th><th>TimesFM</th><th>Error</th><th>Días grandes / evaluados</th></tr></thead><tbody>${rows}</tbody></table></div><p>Error con signo = TimesFM menos Td observada. En ${repeat(c)} de 4 años hubo al menos un día con error absoluto ≥ ${f(threshold,3)} °C. Eso no significa que el error fuera grande todos los días.</p>`;
  }
  function thermal(zone){const code=zone.trim().slice(-2);return {"A'":'cálido',"B'":'templado',"C'":'frío',"D'":'semifrígido',"E'":'frígido'}[code]||'sin clase térmica asignada'}
  function annual(){
    const subset=scope().filter(c=>annualRegion==='peru'||c.depto===selected.depto),four=subset.filter(c=>repeat(c)===4).length;
    $('kc-years-title').textContent=`Picos de error en ${annualRegion==='peru'?'el Perú':title(selected.depto)}, año por año`;
    K.years.forEach((year,i)=>{$('kc-year-note-'+year).textContent=`Máximo: ${f(Math.max(...subset.map(c=>c.max_error[i])))} °C`});
    $('kc-persistence-note').innerHTML=`En <strong>${fmt(four)} de ${fmt(subset.length)} celdas</strong> de esta vista hubo al menos un error absoluto ≥ ${f(threshold,3)} °C en <strong>cada uno de los cuatro años</strong>. Se utiliza el mismo umbral en todos los lugares y años.`;
  }
  function maps(){draw($('kc-map'),period);draw($('kc-inset'),period);K.years.forEach((year,i)=>draw($('kc-year-'+year),String(i)))}
  function topCells(){
    const rank=scope().slice().sort((a,b)=>value(b)-value(a)||b.overall.max_error-a.overall.max_error).slice(0,5);
    $('kc-top-cells').innerHTML=`<h3>${period==='repeat'?'Celdas con más años con errores grandes':'Cinco celdas con los picos más altos'}</h3>`+rank.map(c=>`<button type="button" data-id="${c.id}" aria-pressed="${c.id===selected.id}">${title(c.depto)} · celda ${c.id} · <b>${f(value(c),period==='repeat'?0:2)} ${period==='repeat'?'años':'°C'}</b></button>`).join('');
    $('kc-top-cells').querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>choose(cells.find(c=>c.id===Number(b.dataset.id)))));
  }
  function choose(c){selected=c;zoom=1;center=null;$('kc-cell-details').open=true;render()}
  function render(){
    $('kc-period').value=period;
    $('kc-scope').textContent=`${fmt(scope().length)} celdas del Perú`;
    $('kc-map-title').textContent=period==='repeat'?'En cuántos años hubo un error grande':period==='max'?'El mayor error diario en cada celda, en °C':`El mayor error diario de ${K.years[Number(period)]}, en °C`;
    $('kc-map-sub').textContent=period==='repeat'?`Se cuenta cada año con al menos un error absoluto ≥ ${f(threshold,3)} °C.`:'Un punto más oscuro indica una separación mayor entre TimesFM y la Td observada en el mismo día.';
    $('kc-inset-region').textContent=title(selected.depto)+' · ampliación';
    $('kc-inset-title').textContent=`Celda seleccionada: ${selected.id}`;
    $('kc-legend').innerHTML=period==='repeat'?colors.map((col,i)=>`<span><i style="background:${col}"></i>${i} ${i===1?'año':'años'}</span>`).join(''):legend();
    $('kc-annual-legend').innerHTML=legend();
    $('kc-year-region').querySelector('[value=focus]').textContent=title(selected.depto)+' ampliado';
    annual();maps();detail();topCells();
  }
  function fixedFindings(){
    const worst=cells.find(c=>c.id===K.worst_id),p=peak(worst,peakYear(worst));
    $('kc-headline').textContent=`El mayor pico de error alcanza ${f(Math.abs(p.error))} °C en ${title(worst.depto)}`;
    $('kc-summary').innerHTML=`<div class="kc-result"><h3>Mayor error diario · todo el Perú evaluado</h3><strong>${f(Math.abs(p.error))} °C</strong><p>${title(worst.depto)} · ${date(p.day)} · celda ${worst.id}</p><p>Td observada ${f(p.obs)} °C · TimesFM ${f(p.pred)} °C</p></div><div class="kc-result"><h3>Umbral para localizar errores grandes</h3><strong>≈ ${f(threshold)} °C</strong><p>Por encima de este umbral se encuentra el 1 % de los errores diarios más altos del Perú evaluado.</p><p>Se aplica el mismo valor a todas las celdas y años.</p></div>`;
    $('kc-definition').textContent='Error = TimesFM menos Td observada, en la misma celda y día. Para localizar picos se utiliza su valor absoluto; por ejemplo, estimar 15 °C cuando se observan 20 °C produce un error de −5 °C y una separación de 5 °C.';
    const warm=K.climate.find(c=>c.warm),other=K.climate.find(c=>!c.warm),ratio=warm.rate1000/other.rate1000,scale=Math.ceil(Math.max(warm.rate1000,other.rate1000)/5)*5;
    $('kc-climate-title').textContent=`Los errores grandes son ${f(ratio,1)} veces más frecuentes en climas cálidos`;
    $('kc-climate-bars').innerHTML=[warm,other].map(c=>`<div class="kc-rate-row"><div class="kc-rate-label">${c.warm?"Climas cálidos (A')":'Resto de celdas'}<small>${fmt(c.cells)} celdas · ${fmt(c.n)} pares diarios</small></div><div class="kc-rate-track"><i style="width:${100*c.rate1000/scale}%;background:${c.warm?'#aa512e':'#87999e'}"></i></div><div class="kc-rate-value">${f(c.rate1000,1)}</div></div>`).join('')+`<p class="kc-map-foot">Unidad: errores absolutos ≥ ${f(threshold,3)} °C por cada 1.000 pares diarios. Barras con origen en cero y escala común de 0 a ${scale}.</p>`;
    const zone=K.zones.slice().sort((a,b)=>b.rate1000-a.rate1000)[0];
    $('kc-climate-note').textContent=`En esta muestra, ${f(warm.extreme/(warm.extreme+other.extreme)*100,1)} % de los errores grandes ocurre en climas cálidos, que representan ${f(warm.n/(warm.n+other.n)*100,1)} % de los pares evaluados. Sin embargo, el mayor error de un solo día está en un clima ${thermal(worst.zona)} de ${title(worst.depto)}. La zona con mayor frecuencia es ${zone.zone_label} (${thermal(zone.zone_label)}): ${f(zone.rate1000,1)} por 1.000, sobre ${fmt(zone.cells)} celdas. El resultado agrupado no implica que todas las zonas cálidas tengan más error que todas las demás.`;
  }
  function nearest(event,canvas){const rect=canvas.getBoundingClientRect(),x=(event.clientX-rect.left)*canvas.width/rect.width,y=(event.clientY-rect.top)*canvas.height/rect.height,v=frame(canvas);let best=null,distance=Infinity;for(const c of scope()){if((v.local&&c.depto!==selected.depto)||!inside(c,v))continue;const[cx,cy]=v.xy(c.lon,c.lat),d=Math.hypot(cx-x,cy-y);if(d<distance){distance=d;best=c}}return distance<9*canvas.width/rect.width?best:null}
  let drag=null,suppress=false;
  $('kc-map').addEventListener('pointerdown',e=>{if(e.pointerType==='touch')return;const v=frame($('kc-map'));drag={x:e.clientX,y:e.clientY,mid:[...v.mid],dx:v.dx,dy:v.dy};suppress=false;$('kc-map').setPointerCapture(e.pointerId)});
  $('kc-map').addEventListener('pointermove',e=>{if(!drag)return;const dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(Math.hypot(dx,dy)<5&&!suppress)return;suppress=true;const r=$('kc-map').getBoundingClientRect();center=[drag.mid[0]-dx/r.width*drag.dx,drag.mid[1]+dy/r.height*drag.dy];draw($('kc-map'),period)});
  $('kc-map').addEventListener('pointerup',()=>drag=null);$('kc-map').addEventListener('pointercancel',()=>{drag=null;suppress=false});
  for(const id of['kc-map','kc-inset',...K.years.map(y=>'kc-year-'+y)])$(id).addEventListener('click',e=>{if(id==='kc-map'&&suppress){suppress=false;return}const c=nearest(e,$(id));if(!c)return;if(id.startsWith('kc-year-'))period=String(K.years.indexOf(Number(id.slice(8))));choose(c)});
  $('kc-climate-filter').addEventListener('change',e=>{climate=e.target.value;selected=scope().slice().sort((a,b)=>b.overall.max_error-a.overall.max_error)[0];zoom=1;center=null;render()});
  $('kc-period').addEventListener('change',e=>{period=e.target.value;render()});
  $('kc-year-region').addEventListener('change',e=>{annualRegion=e.target.value;annual();maps()});
  $('kc-zoom-in').addEventListener('click',()=>{center=[selected.lon,selected.lat];zoom=Math.min(12,zoom*1.6);maps()});
  $('kc-zoom-out').addEventListener('click',()=>{zoom=Math.max(1,zoom/1.6);if(zoom===1)center=null;maps()});
  $('kc-reset').addEventListener('click',()=>{zoom=1;center=null;maps()});
  new ResizeObserver(()=>maps()).observe($('kc-map').parentElement);
  fixedFindings();render();
})();
