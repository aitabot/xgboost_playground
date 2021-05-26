import os

import dotenv
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
from pandas import DataFrame

dotenv.load_dotenv()
filename = "data_thomas.csv"
key = os.environ['KEY']
symbol = 'AMD'
output_size = 'full'

ts = TimeSeries(key=key, output_format='pandas')
ti = TechIndicators(key=os.environ['KEY'], output_format='pandas')
df = ts.get_daily_adjusted(symbol, output_size)[0].sort_index(axis=0, ascending=True)
df = DataFrame(df)

ti = TechIndicators(key=key, output_format='pandas')
sma_time_period = 20
ema_time_period = 20
rsi_time_period = 20
roc_time_period = 1
adx_time_period = 20
cci_time_period = 20
aroon_time_period = 20
bbands_time_period = 20

df['roc'], _ = ti.get_roc(symbol=symbol, time_period=roc_time_period)
df['sma'], _ = ti.get_sma(symbol=symbol, time_period=sma_time_period)
df['ema'], _ = ti.get_ema(symbol=symbol, time_period=ema_time_period)
df['rsi'], _ = ti.get_rsi(symbol=symbol, time_period=rsi_time_period)
df['obv'], _ = ti.get_obv(symbol=symbol)
macd = ti.get_macd(symbol=symbol)[0].sort_index(axis=0, ascending=True)
for column in macd.columns:
    df[column] = macd[column]

stoch = ti.get_stoch(symbol=symbol)[0].sort_index(axis=0, ascending=True)
for column in stoch.columns:
    df[column] = stoch[column]

df['adx'], _ = ti.get_adx(symbol=symbol, time_period=adx_time_period)
df['cci'], _ = ti.get_cci(symbol=symbol, time_period=cci_time_period)
aroon = ti.get_aroon(symbol=symbol, time_period=aroon_time_period)[0].sort_index(axis=0, ascending=True)
for column in aroon.columns:
    df[column] = aroon[column]

bbands = ti.get_bbands(symbol=symbol, time_period=bbands_time_period)[0].sort_index(axis=0, ascending=True)
for column in bbands.columns:
    df[column] = bbands[column]

df['ad'], _ = ti.get_ad(symbol=symbol)

df['shifted_ROC_BOOL'] = (df['roc'].shift(-1) >= 0).astype(int)

df.to_csv(filename)
