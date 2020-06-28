# Do necessary Imports
import os
import numpy as np
import pandas as pd
from pathlib import Path
import quandl

# Read BSE 500 Constituents csv file
bse500_metadata = pd.read_csv('S&P_bse500.csv')
print(bse500_metadata.head(2))

# Get all 500+ tickers
tickers = list(bse500_metadata['Scrip Code'])  # Input your quandl key
quandl.ApiConfig.api_key = '<Your API Key>'  # Start Bulk download in a loop and create a Dataframedef get(tickers):
print(tickers[:2])

stray_tickers = []
available_tickers = []

def get(tickers):

    def quandl_fetch(ticker):
        try:
            print('Processing…, BSE/BOM', ticker)
            return quandl.get('BSE/BOM' + str(ticker))
        except:
            print('Error fetching ' + str(ticker))
            stray_tickers.append(ticker)
            return None

    all_ticker_data = [quandl_fetch(ticker) for ticker in tickers if
                       quandl_fetch(ticker) is not None]  # map(quandl_fetch, tickers)
    available_tickers.extend([t for t in tickers if t not in stray_tickers])
    return pd.concat(all_ticker_data, keys=available_tickers, names=['ticker', 'date'])


df = get(tickers)
# filter required columns from Dataframe
columns = ['Open', 'High', 'Low', 'Close', 'No. of Trades']  # Rename the columns as per zipline requirement
prices = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume'])
prices['open'] = df['Open'];
prices['high'] = df['High'];
prices['low'] = df['Low'];
prices['close'] = df['Close'];
prices['volume'] = df['No. of Trades'];

# Write a csv file for each ticker
for ticker in available_tickers:
    df = prices.loc[ticker]
    filename = 'bse500/' + str(ticker) + '.csv'
    df.to_csv(filename, index=True)
