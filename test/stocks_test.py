



from pandas import DataFrame
from app.trend_chart import fetch_stocks_json
import requests
import json

def test_example():
    assert 2 + 2 == 4


def test_data_fetching():

    df = fetch_stocks_json("MSFT")
    assert isinstance(df, DataFrame)
    assert df.columns.tolist() == ["timestamp", "open", "high", "low", "close", "adjusted_close", "volume", "dividend_amount", "split_coefficient"]
    assert len(df) > 1500

    earliest = df.iloc[-1]
    assert earliest["timestamp"] == '2018-04-03'
    assert earliest["adjusted_close"] == 149.01

