import numpy as np, pandas as pd
S='/tmp/claude-1001/-home-cvelasquez-Code-tdew/5634240d-3cdc-4674-a678-09aa23e48ae8/scratchpad'
TD=np.load(f'{S}/TD.npy').astype('f8'); TM=np.load(f'{S}/TM.npy').astype('f8'); ids=np.load(f'{S}/ids.npy')
dates=pd.date_range('1981-01-01','2016-12-31'); doy=dates.dayofyear.to_numpy(); yr=dates.year.to_numpy()
def clim(X,mask):
    out=np.zeros((X.shape[0],367))
    for d in range(1,367):
        m=mask&(doy==d); out[:,d]=X[:,m].mean(1)
    return out
def fit(tr_mask,h,Ctd,Ctm):
    # returns a[c,d], b[c,d] for anomaly regression with tricube circular window over doy 1..366
    xa=TM-Ctm[:,doy]; ya=TD-Ctd[:,doy]
    sums={k:np.zeros((TD.shape[0],366)) for k in ('n','x','y','xx','xy')}
    for d in range(1,367):
        m=tr_mask&(doy==d)
        x=xa[:,m]; y=ya[:,m]
        sums['n'][:,d-1]=m.sum(); sums['x'][:,d-1]=x.sum(1); sums['y'][:,d-1]=y.sum(1)
        sums['xx'][:,d-1]=(x*x).sum(1); sums['xy'][:,d-1]=(x*y).sum(1)
    ks=np.arange(-h,h+1); w=(1-(np.abs(ks)/(h+1))**3)**3
    W={}
    for k,v in sums.items():
        acc=np.zeros_like(v)
        for kk,ww in zip(ks,w): acc+=ww*np.roll(v,-kk,axis=1)
        W[k]=acc
    n,x,y,xx,xy=W['n'],W['x'],W['y'],W['xx'],W['xy']
    den=n*xx-x*x+1e-9; b=(n*xy-x*y)/den; a=(y-b*x)/n
    return a,b
def predict(a,b,Ctd,Ctm,mask):
    cols=np.where(mask)[0]; d=doy[cols]-1
    xa=TM[:,cols]-Ctm[:,doy[cols]]
    return Ctd[:,doy[cols]]+a[:,d]+b[:,d]*xa, TD[:,cols]
# validation: fit 1981-2008, test 2009-2012
tr=yr<=2008; va=(yr>=2009)&(yr<=2012)
Ctd=clim(TD,tr); Ctm=clim(TM,tr)
res={}
for h in (7,11,15,21,31,45,60):
    a,b=fit(tr,h,Ctd,Ctm); p,o=predict(a,b,Ctd,Ctm,va); res[h]=np.sqrt(np.mean((p-o)**2))
    print('val h',h,res[h])
hbest=min(res,key=res.get); print('hbest (train-only validation)',hbest)
# climatology-only on val
cp=Ctd[:,doy[va]]; print('val clim',np.sqrt(np.mean((cp-TD[:,va])**2)))
# final: fit 1981-2012, test 2013-2016
tr=yr<=2012; te=yr>=2013
Ctd=clim(TD,tr); Ctm=clim(TM,tr)
pq=pd.read_parquet('/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/ll4/predictions.parquet',columns=['ID','FECHA','TD_obs','pred_tuned','pred_clim','pred_timesfm'])
cell=pd.Series(np.arange(len(ids)),index=ids)
r=cell.reindex(pq.ID.values).to_numpy(); c=((pq.FECHA-dates[0]).dt.days).to_numpy()
o=pq.TD_obs.to_numpy('f8'); print('obs check',np.abs(TD[r,c]-o).max())
cl=Ctd[r,doy[c]]; print('clim check',np.abs(cl-pq.pred_clim.to_numpy('f8')).max())
t=pq.pred_timesfm.to_numpy('f8'); p=pq.pred_tuned.to_numpy('f8'); y=pq.FECHA.dt.year.to_numpy()
def rep(name,v):
    s=lambda m: np.sqrt(np.mean((v[m]-o[m])**2))
    print(f'{name:28s} all {s(y>0):.4f}  13-14 {s(y<=2014):.4f}  15-16 {s(y>=2015):.4f}  bias {np.mean(v-o):+.3f}')
rep('timesfm',t); rep('palacios tuned',p); rep('clim',cl)
for h in (7,11,15,21,31,45,60):
    a,b=fit(tr,h,Ctd,Ctm)
    v=Ctd[r,doy[c]]+a[r,doy[c]-1]+b[r,doy[c]-1]*(TM[r,c]-Ctm[r,doy[c]])
    rep(f'direct Tmin-LLR h={h}',v)
    if h==hbest: vb=v
# Tmin anomaly only cell-global OLS
xa=TM-Ctm[:,doy]; ya=TD-Ctd[:,doy]
xs=xa[:,tr]; ys=ya[:,tr]; b=((xs*ys).mean(1)-xs.mean(1)*ys.mean(1))/xs.var(1); a=ys.mean(1)-b*xs.mean(1)
v=cl+a[r]+b[r]*(TM[r,c]-Ctm[r,doy[c]]); rep('direct cell OLS (no doy)',v)
rep('direct Tmin-LLR hbest + TFM avg',0.5*vb+0.5*t)
# how many TFM-vs-direct by cell
np.save(f'{S}/vb.npy',vb)
# paired by year
for yy in (2013,2014,2015,2016):
    m=y==yy; print(yy,'tfm',np.sqrt(np.mean((t[m]-o[m])**2)),'pal',np.sqrt(np.mean((p[m]-o[m])**2)),'direct',np.sqrt(np.mean((vb[m]-o[m])**2)))
# mean-level decomposition: cell-year mean error
df=pd.DataFrame({'ID':pq.ID.values,'y':y,'et':t-o,'ep':p-o,'ed':vb-o})
g=df.groupby(['ID','y'])[['et','ep','ed']].transform('mean')
for k in ('et','ep','ed'): print(k,'MSE',np.mean(df[k]**2),'cell-year-mean^2',np.mean(g[k]**2),'within',np.mean((df[k]-g[k])**2))
