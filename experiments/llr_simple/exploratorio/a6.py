import numpy as np, pandas as pd, glob, os
S='/tmp/claude-1001/-home-cvelasquez-Code-tdew/5634240d-3cdc-4674-a678-09aa23e48ae8/scratchpad'
ref=pd.read_parquet('/home/cvelasquez/tdew_timesfm/backtest_clean_timesfm/ll4/predictions.parquet',columns=['ID','FECHA','TD_obs','pred_tuned','pred_clim'])
vb=np.load(f'{S}/vb.npy'); ref['direct']=vb
cr=set(pd.read_csv('reports/timesfm_benchmark/panels/cribado_estratificado.csv').ID)
ref=ref[ref.ID.isin(cr)]
rows=[]
for f in sorted(glob.glob('/home/cvelasquez/tdew_timesfm/preds_cribado/ll4__*.parquet')):
    k=os.path.basename(f)[5:-8]
    p=pd.read_parquet(f,columns=['ID','FECHA','pred']); p['FECHA']=pd.to_datetime(p.FECHA)
    m=ref.merge(p,on=['ID','FECHA'])
    r=lambda c:np.sqrt(np.mean((m[c]-m.TD_obs)**2))
    # per-cell paired diff TFM - direct
    rows.append((k,m.ID.nunique(),r('pred'),r('pred_tuned'),r('direct'),r('pred_clim')))
d=pd.DataFrame(rows,columns=['var','cells','tfm','palacios','direct','clim']).sort_values('tfm'); d['tfm-direct']=d.direct-d.tfm
print(d.to_string())
