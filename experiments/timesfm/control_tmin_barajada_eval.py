import numpy as np, pandas as pd
W='/home/cvelasquez/tdew_timesfm'
R='/media/ppalacios/Data1/henry_simcast_peru_full/results_tuning/tuning/backtest_clean/ll4/predictions.parquet'
ref=pd.read_parquet(R,columns=['ID','FECHA','TD_obs','pred_clim','pred_tuned'])
out=ref
for tag,path in [('real_td','preds_cribado/ll4__tmin_td_full'),('shuf_td','preds_cribado_shuffle_year/ll4__tmin_td_full'),
                 ('real_anom','preds_cribado/ll4__tmin_anom_full'),('shuf_anom','preds_cribado_shuffle_year/ll4__tmin_anom_full')]:
    d=pd.read_parquet(f'{W}/{path}.parquet',columns=['ID','FECHA','pred']).rename(columns={'pred':tag})
    out=out.merge(d,on=['ID','FECHA'],how='inner')
print('celdas',out.ID.nunique(),'filas',len(out))
o=out.TD_obs.to_numpy('f8')
rm=lambda c: float(np.sqrt(np.mean((out[c].to_numpy('f8')-o)**2)))
cl=rm('pred_clim')
for c in ['pred_clim','pred_tuned','real_td','shuf_td','real_anom','shuf_anom']:
    r=rm(c); print(f'{c:12s} rmse {r:.4f}  skill {1-r/cl:+.3f}  bias {np.mean(out[c]-o):+.3f}')
