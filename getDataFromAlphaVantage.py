import csv
import os
from datetime import date
from typing import List

import pandas as pd
import numpy as np
from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries


def load_time_series(symbol: str, output_size="full") -> pd.DataFrame:
    """Get Time_Series_Data from AlphaVantage and returns it.

    Args:
        symbol (str): The Stock Symbol you're looking for.
        output_size (str, optional): "compact" or "full". Defaults to "full".

    Returns:
        List of Prices.
    """
    ts = TimeSeries(key=os.environ['KEY'], output_format='pandas')
    res, _ = ts.get_daily_adjusted(symbol, output_size)
    return res


def get_indicators(symbol: str, data=pd.DataFrame):
    ti = TechIndicators(key=os.environ['KEY'], output_format='pandas')
    sma_time_period = 20
    ema_time_period = 21
    rsi_time_period = 14
    roc_time_period = 1

    sma, _ = ti.get_sma(symbol=symbol, time_period=sma_time_period)
    sma = sma.sort_values(['date'], ascending=[False])
    data[f'SMA_{sma_time_period}'] = sma['SMA']

    ema, _ = ti.get_ema(symbol=symbol, time_period=ema_time_period)
    ema = ema.sort_values(['date'], ascending=[False])
    data[f'EMA_{ema_time_period}'] = ema['EMA']

    # Positive when (the fast)SMA > (the slower)EMA
    # Generally it shows where support is in an up treand
    # or resistance when in an down trend
    data[f'SMA_{sma_time_period}_gt_EMA{ema_time_period}'] = np.where(
        data[f'SMA_{sma_time_period}'] >= data[f'EMA_{ema_time_period}'], 1.0, 0.0
    )

    rsi, _ = ti.get_rsi(symbol=symbol, time_period=rsi_time_period)
    rsi = rsi.sort_values(['date'], ascending=[False])
    data[f'RSI_{rsi_time_period}'] = rsi['RSI']

    obv, _ = ti.get_obv(symbol=symbol)
    obv = obv.sort_values(['date'], ascending=[False])
    data['OBV'] = obv['OBV']

    roc, _ = ti.get_roc(symbol=symbol, time_period=roc_time_period)
    roc = roc.sort_values(['date'], ascending=[False])
    data[f'ROC_{roc_time_period}'] = roc['ROC']

    return data


if __name__ == '__main__':
    """
    Set the variable `symbol` to whatever you're looking for.
    """
    symbol = "AMD"
    filename = f'./data-{symbol}-{date.today()}.csv'
    data: pd.DataFrame = load_time_series(symbol=symbol)
    data.drop(['4. close', '7. dividend amount',
              '8. split coefficient'], axis=1, inplace=True)
    data: pd.DataFrame = get_indicators(symbol=symbol, data=data)

    data.columns = data.columns.str.replace(' ', '_')
    data.columns = data.columns.str.replace('[0-9]\.\_', '')

    if os.path.isfile(filename):
        os.remove(filename)

    data.to_csv(filename)
