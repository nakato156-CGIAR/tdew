import numpy as np, pandas as pd, pyarrow.parquet as pq, pyarrow as pa, time
from concurrent.futures import ThreadPoolExecutor
R='/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning'
S='/tmp/claude-1001/-home-cvelasquez-Code-tdew/5634240d-3cdc-4674-a678-09aa23e48ae8/scratchpad'
ids=pd.read_csv('reports/timesfm_benchmark/panels/nacional_17027.csv').ID.to_numpy()
cellidx={int(i):k for k,i in enumerate(ids)}
dates=pd.date_range('1981-01-01','2016-12-31'); T=len(dates)
TD=np.full((len(ids),T),np.nan,'f4'); TM=np.full((len(ids),T),np.nan,'f4')
dpos={d:i for i,d in enumerate(dates)}
byb={}
for i in ids: byb.setdefault(int(i)%8192,[]).append(int(i))
def load(b):
    out=[]
    for yr in range(1981,2017):
        t=pd.read_parquet(f'{R}/bucketed_training_data/id_bucket={b:04d}/train_{yr}.parquet',columns=['ID','FECHA','TD','TMIN'])
        t=t[t.ID.isin(byb[b])]; out.append(t)
    return pd.concat(out)
t0=time.time()
with ThreadPoolExecutor(16) as ex:
    for t in ex.map(load,sorted(byb)):
        r=t.ID.map(cellidx).to_numpy(); c=((pd.to_datetime(t.FECHA)-dates[0]).dt.days).to_numpy()
        TD[r,c]=t.TD.to_numpy(); TM[r,c]=t.TMIN.to_numpy()
print('loaded',time.time()-t0,np.isnan(TD).mean(),np.isnan(TM).mean())
np.save(f'{S}/TD.npy',TD); np.save(f'{S}/TM.npy',TM); np.save(f'{S}/ids.npy',ids)
