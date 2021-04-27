import csv
import os
from typing import List
from datetime import date

from alpha_vantage.fundamentaldata import FundamentalData
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries


def load_time_series(symbol: str, output_size="full") -> List:
    """Get Time_Series_Data from AlphaVantage and returns it.

    Args:
        symbol (str): The Stock Symbol you're looking for.
        output_size (str, optional): "compact" or "full". Defaults to "full".

    Returns:
        List of Prices.
    """
    ts = TimeSeries(key=os.environ['KEY'], output_format='csv')
    res, _ = ts.get_daily_adjusted(symbol, output_size)
    return res


if __name__ == '__main__':
    """
    Set the variable `symbol` to whatever you're looking for.
    """
    symbol = "AMD"
    filename = f'./data-{symbol}-{date.today()}.csv'
    data = load_time_series(symbol)

    if os.path.isfile(filename):
        os.remove(filename)

    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)
