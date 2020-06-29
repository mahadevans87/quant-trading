# Do necessary Imports
import os
import numpy as np
import pandas as pd
from pathlib import Path
import yfinance as yf

# Read BSE 500 Constituents csv file
nse500_metadata = pd.read_csv('ind_nifty500list.csv')
# print(bse500_metadata.head(2))

# Get all 500+ tickers
tickers = list(nse500_metadata['Symbol'])


# print(tickers[:2])


def get(tickers):
    def yahoo_fetch(ticker):
        print('Processing…, NSE ', ticker)
        return yf.download(ticker + '.NS', progress=True, actions=True)

    all_ticker_data = [yahoo_fetch(ticker) for ticker in tickers]
    return pd.concat(all_ticker_data, keys=tickers, names=['ticker', 'date'])


df = get(tickers)

# filter required columns from Dataframe
columns = ['Open', 'High', 'Low', 'Close', 'No. of Trades']  # Rename the columns as per zipline requirement
prices = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
prices['open'] = df['Open'];
prices['high'] = df['High'];
prices['low'] = df['Low'];
prices['close'] = df['Adj Close'];
prices['volume'] = df['Volume'];
prices['dividend'] = df['Dividends']
prices['split'] = df['Stock Splits']




#Write a csv file for each ticker
for ticker in tickers:
    df = prices.loc[ticker]
    df = df[~df.index.duplicated()]
    df = df.asfreq('D', method='ffill').dropna()
    filename = 'nse500/' + ticker + '.csv'
    df.to_csv(filename, index=True)
