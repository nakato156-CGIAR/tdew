import numpy as np, pandas as pd
R='/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning'
df=pd.read_parquet('/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/ll4/predictions.parquet',
  columns=['ID','zone_id','FECHA','doy','TD_obs','pred_tuned','pred_clim','pred_timesfm'])
z=pd.read_parquet(f'{R}/zone_table.parquet',columns=['ID','lon','lat'])
df=df.merge(z,on='ID',how='left')
df['year']=df.FECHA.dt.year; df['month']=df.FECHA.dt.month
o=df.TD_obs.to_numpy('f8'); c=df.pred_clim.to_numpy('f8')
P={'tfm':df.pred_timesfm.to_numpy('f8'),'pal':df.pred_tuned.to_numpy('f8'),'clim':c}
oa=o-c
def rm(x): return np.sqrt(np.mean(x))
for k,v in P.items(): print(k,'rmse',rm((v-o)**2),'bias',(v-o).mean())
et={k:(v-o) for k,v in P.items()}
d=et['pal']**2-et['tfm']**2   # >0 TimesFM better
df['d']=d; df['se_t']=et['tfm']**2; df['se_p']=et['pal']**2; df['se_c']=et['clim']**2
df['e_t']=et['tfm']; df['e_p']=et['pal']; df['oa']=oa
print('NaN counts',df[['pred_timesfm','pred_tuned']].isna().sum().to_dict())
# bias/variance decomposition: per-cell bias, per-cell-month bias
for k in ['tfm','pal']:
    e=pd.Series(et[k]); 
    cb=e.groupby(df.ID.values).transform('mean'); 
    cmb=e.groupby([df.ID.values,df.month.values]).transform('mean')
    print(k,'MSE',np.mean(e**2),'cell-bias^2',np.mean(cb**2),'cell-month-bias^2',np.mean(cmb**2),'resid var',np.mean((e-cmb)**2),'pooled bias^2',e.mean()**2)
# amplitude: regression slope of pred anomaly on obs anomaly and corr
for k in ['tfm','pal']:
    pa=P[k]-c
    print(k,'slope pa~oa',np.cov(pa,oa)[0,1]/oa.var(),'corr',np.corrcoef(pa,oa)[0,1],'std pa',pa.std(),'std oa',oa.std())
# by year / month
print(df.groupby('year')[['se_t','se_p','se_c']].mean().pow(.5).assign(gap=lambda x:x.se_p-x.se_t))
print(df.groupby('month')[['se_t','se_p','se_c']].mean().pow(.5).assign(gap=lambda x:x.se_p-x.se_t))
# by obs anomaly magnitude bin (cell-level std standardized)
sd=df.groupby('ID').oa.transform('std'); zs=(df.oa/sd)
bins=pd.cut(zs,[-99,-3,-2,-1,1,2,3,99])
print(df.groupby(bins,observed=True)[['se_t','se_p']].agg(['mean','size']).pipe(lambda x:x))
print('share of total SE diff from |z|>2:', d[np.abs(zs)>2].sum()/d.sum(), 'frac obs',np.mean(np.abs(zs)>2))
# horizon day-of-block: ΔMSE by horizon quarter
df['hday']=(df.FECHA-pd.Timestamp('2013-01-01')).dt.days
print(df.groupby(pd.cut(df.hday,[-1,30,90,180,365,730,1100,1461]),observed=True)[['se_t','se_p','se_c']].mean().pow(.5).assign(gap=lambda x:x.se_p-x.se_t))
# per-cell gap
cell=df.groupby('ID').agg(se_t=('se_t','mean'),se_p=('se_p','mean'),zone=('zone_id','first'),lon=('lon','first'),lat=('lat','first'))
cell['dm']=cell.se_p-cell.se_t
cell['in_peru']=np.nan
print('cells TFM better MSE',(cell.dm>0).mean(),'n',len(cell))
zg=cell.groupby('zone').agg(n=('dm','size'),mse_t=('se_t','mean'),mse_p=('se_p','mean'))
zg['rt']=zg.mse_t**.5; zg['rp']=zg.mse_p**.5; zg['gap']=zg.rp-zg.rt
print(zg.sort_values('n').to_string())
print('zones TFM better',(zg.gap>0).sum(),'of',len(zg))
# spatial block bootstrap on cell-level mean MSE diff
cell['bx']=np.floor(cell.lon/2).astype(int); cell['by']=np.floor(cell.lat/2).astype(int)
cell['blk']=cell.bx.astype(str)+'_'+cell.by.astype(str)
g=cell.groupby('blk').agg(n=('dm','size'),sp=('se_p','sum'),st=('se_t','sum'))
print('blocks 2deg',len(g))
rng=np.random.default_rng(0); B=2000; r=[]
n=g.n.to_numpy(); sp=g.sp.to_numpy(); st=g.st.to_numpy()
for _ in range(B):
    i=rng.integers(0,len(g),len(g)); N=n[i].sum()
    r.append(np.sqrt(sp[i].sum()/N)-np.sqrt(st[i].sum()/N))
print('2deg block-bootstrap dRMSE CI',np.percentile(r,[2.5,50,97.5]),'point',np.sqrt(cell.se_p.mean())-np.sqrt(cell.se_t.mean()))
for deg in (1,5):
    bk=(np.floor(cell.lon/deg).astype(int).astype(str)+'_'+np.floor(cell.lat/deg).astype(int).astype(str))
    g2=cell.groupby(bk).agg(n=('dm','size'),sp=('se_p','sum'),st=('se_t','sum')); n=g2.n.to_numpy(); sp=g2.sp.to_numpy(); st=g2.st.to_numpy(); r=[]
    for _ in range(B):
        i=rng.integers(0,len(g2),len(g2)); N=n[i].sum(); r.append(np.sqrt(sp[i].sum()/N)-np.sqrt(st[i].sum()/N))
    print(deg,'deg blocks',len(g2),np.percentile(r,[2.5,97.5]))
# year-block + spatial: dRMSE by year (4 values) share
yy=df.groupby('year').agg(sp=('se_p','mean'),st=('se_t','mean'))
print('yearly dRMSE',(yy.sp**.5-yy.st**.5).to_dict())
# time-block bootstrap by month-year (48 blocks) for pooled dMSE
my=df.groupby(['year','month']).agg(n=('d','size'),sp=('se_p','sum'),st=('se_t','sum'))
n=my.n.to_numpy(); sp=my.sp.to_numpy(); st=my.st.to_numpy(); r=[]
for _ in range(B):
    i=rng.integers(0,len(my),len(my)); N=n[i].sum(); r.append(np.sqrt(sp[i].sum()/N)-np.sqrt(st[i].sum()/N))
print('month-year block bootstrap',np.percentile(r,[2.5,97.5]),'months where TFM better',((my.sp>my.st).sum()),'of',len(my))
cell.to_parquet('/tmp/claude-1001/-home-cvelasquez-Code-tdew/5634240d-3cdc-4674-a678-09aa23e48ae8/scratchpad/cell.parquet')
# Peru? skip. Outside/inside via lon/lat rough: leave
# lat-lon dependency of gap
print(cell.groupby(pd.cut(cell.lat,[-20,-15,-10,-5,0,5])).agg(n=('dm','size'),sp=('se_p','mean'),st=('se_t','mean')).assign(g=lambda x:x.sp**.5-x.st**.5))
