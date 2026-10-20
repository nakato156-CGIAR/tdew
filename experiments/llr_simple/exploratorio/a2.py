import numpy as np, pandas as pd
df=pd.read_parquet('/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/ll4/predictions.parquet',
  columns=['ID','FECHA','TD_obs','pred_tuned','pred_clim','pred_timesfm','Tmin_hold','doy'])
y=df.FECHA.dt.year.to_numpy()
o=df.TD_obs.to_numpy('f8'); c=df.pred_clim.to_numpy('f8'); t=df.pred_timesfm.to_numpy('f8'); p=df.pred_tuned.to_numpy('f8')
def r(m): return np.sqrt(np.mean(((t if m=='t' else p if m=='p' else c)[sel]-o[sel])**2))
for name,sel in [('2013-14',y<=2014),('2015-16',y>=2015),('2013',y==2013),('2014',y==2014),('2015',y==2015),('2016',y==2016)]:
    print(name,'tfm',r('t'),'pal',r('p'),'clim',r('c'),'gap',r('p')-r('t'),'skill tfm',1-r('t')/r('c'),'skill pal',1-r('p')/r('c'))
# oracle linear recalibration of anomaly: obs_anom ~ a + b*pred_anom (global, then per-year)
oa=o-c
for nm,v in (('tfm',t),('pal',p)):
    pa=v-c; b=np.cov(pa,oa)[0,1]/pa.var(); a=oa.mean()-b*pa.mean()
    print(nm,'oracle recal slope',b,'intercept',a,'rmse',np.sqrt(np.mean((oa-(a+b*pa))**2)))
# shrunk/inflated combos: tfm damped to Palacios amplitude and vice versa
pat=t-c; pap=p-c
for k in (0.6,0.7,0.77,1.0):
    print('tfm anom scaled',k,np.sqrt(np.mean((c+k*pat-o)**2)))
for k in (1.0,1.25,1.5,1.75):
    print('pal anom scaled',k,np.sqrt(np.mean((c+k*pap-o)**2)))
# blend
for w in (0,0.25,0.5,0.75,1):
    print('blend w_tfm',w,np.sqrt(np.mean((w*t+(1-w)*p-o)**2)))
# Tmin anomaly amplitude: corr of obs anomaly with Tmin anomaly (cell-doy climatology of Tmin from holdout? skip)
# per-year slope
for yy in (2013,2014,2015,2016):
    s=y==yy
    for nm,v in (('tfm',t),('pal',p)):
        pa=(v-c)[s]; b=np.cov(pa,oa[s])[0,1]/pa.var()
        print(yy,nm,'slope',round(b,3),'mean pa',round(pa.mean(),3),'mean oa',round(oa[s].mean(),3))
