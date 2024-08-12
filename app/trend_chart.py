# imports

import os
from pprint import pprint
from statistics import mean
from plotly.express import line
from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
from pandas import read_csv
import requests
import json

#Key & Inputs
load_dotenv()

API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", default="demo")

symbol = input("Enter a Stock Symbol: ")
print("SYMBOL:", symbol)

# Data gathering

if __name__ == "__main__":

    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=15min&outputsize=full&apikey={API_KEY}"
    
    response = requests.get(request_url)
    
    parsed_response = json.loads(response.text)
    tsd = parsed_response['Time Series (15min)']
    dates = list(tsd.keys())
    
    clean_data = []
    
    for k,v in tsd.items():
        record = {
            "date": k,
            "open": float(v["1. open"]),
            "high": float(v["2. high"]),
            "low": float(v["3. low"]),
            "close": float(v["4. close"]),
            "volume": float(v["5. volume"])
        }
        clean_data.append(record)
    
    # VWAP
    
    VWAP_url = f'https://www.alphavantage.co/query?function=VWAP&symbol={symbol}&interval=15min&apikey={API_KEY}'
    VWAP_r = requests.get(VWAP_url)
    VWAP_data = VWAP_r.json()
    vwap = VWAP_data['Technical Analysis: VWAP']
    vwap_dates = list(vwap.keys())
    
    clean_vwap = []
    
    for k, v in vwap.items():
        record = {
            "date": k,
            "VWAP": float(v["VWAP"]),
        }
        clean_vwap.append(record)
    
    # BBANDS
    
    BBand_url = f'https://www.alphavantage.co/query?function=BBANDS&symbol={symbol}&interval=15min&time_period=300&series_type=close&nbdevup=3&nbdevdn=3&apikey={API_KEY}'
    BBand_r = requests.get(BBand_url)
    BBand_data = BBand_r.json()
    bband = BBand_data['Technical Analysis: BBANDS']
    bband_dates = list(bband.keys())
    
    clean_bband = []
    
    for k, v in bband.items():
        record = {
            "date": k,
            "Upper": float(v["Real Upper Band"]),
            "Lower": float(v["Real Lower Band"]),
            "Middle": float(v["Real Middle Band"]),
        }
        clean_bband.append(record)
    
    
    #OHLC Chart
    
    df = DataFrame(clean_data)
    df2 = DataFrame(clean_vwap)
    df3 = DataFrame(clean_bband)
    
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    )])
    
    fig.add_trace(go.Scatter(x=df2['date'],
                          y=df2["VWAP"],
                          name='VWAP',
                          ))
    
    fig.add_trace(go.Scatter(x=df3['date'],
                          y=df3["Upper"],
                          name='BBand Upper'
                          ))
    fig.add_trace(go.Scatter(x=df3['date'],
                          y=df3["Lower"],
                          name='BBand Lower'
                          ))
    fig.add_trace(go.Scatter(x=df3['date'],
                          y=df3["Middle"],
                          name='BBand Middle'
                          ))
    
    fig.update_layout(
        title=f'{symbol} Daily Prices',
        xaxis_title='Date',
        yaxis=dict(title='Price ($)'),
        )
    
    fig.show()


