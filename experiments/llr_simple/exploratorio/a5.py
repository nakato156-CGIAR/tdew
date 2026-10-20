import numpy as np, pandas as pd
S='/tmp/claude-1001/-home-cvelasquez-Code-tdew/5634240d-3cdc-4674-a678-09aa23e48ae8/scratchpad'
vb=np.load(f'{S}/vb.npy')
pq=pd.read_parquet('/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/ll4/predictions.parquet',columns=['ID','zone_id','FECHA','TD_obs','pred_tuned','pred_timesfm'])
z=pd.read_parquet('/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/zone_table.parquet',columns=['ID','lon','lat'])
pq=pq.merge(z,on='ID',how='left')
pq['sd']=(vb-pq.TD_obs)**2; pq['st']=(pq.pred_timesfm-pq.TD_obs)**2; pq['sp']=(pq.pred_tuned-pq.TD_obs)**2
pq['y']=pq.FECHA.dt.year; pq['m']=pq.FECHA.dt.month
cell=pq.groupby('ID').agg(sd=('sd','mean'),st=('st','mean'),sp=('sp','mean'),zone=('zone_id','first'),lon=('lon','first'),lat=('lat','first'))
print('cells where TFM beats direct',(cell.st<cell.sd).mean(),' beats Pal',(cell.st<cell.sp).mean(),' direct beats Pal',(cell.sd<cell.sp).mean())
zz=cell.groupby('zone')[['sd','st','sp']].mean(); print('zones TFM<direct',(zz.st<zz.sd).sum(),'/',len(zz),' direct<Pal',(zz.sd<zz.sp).sum())
rng=np.random.default_rng(1)
def boot(keys,a,b,B=2000):
    g=pq.groupby(keys).agg(n=('sd','size'),a=(a,'sum'),b=(b,'sum')); n=g.n.values;A=g.a.values;Bv=g.b.values
    r=[]
    for _ in range(B):
        i=rng.integers(0,len(g),len(g));N=n[i].sum(); r.append(np.sqrt(A[i].sum()/N)-np.sqrt(Bv[i].sum()/N))
    return len(g),np.percentile(r,[2.5,97.5])
pq['blk']=np.floor(pq.lon/2).astype(int).astype(str)+'_'+np.floor(pq.lat/2).astype(int).astype(str)
for a,b,lab in (('sd','st','direct - TFM'),('sp','sd','Pal - direct'),('sp','st','Pal - TFM')):
    print(lab,'point',np.sqrt(pq[a].mean())-np.sqrt(pq[b].mean()))
    print('  2deg blocks',boot('blk',a,b)); print('  month-year blocks',boot(['y','m'],a,b))
# joint space-time block: resample spatial blocks and years independently? use year resample x block (cluster by year)
print('by year',pq.groupby('y')[['sd','st','sp']].mean().pow(.5).to_dict())
