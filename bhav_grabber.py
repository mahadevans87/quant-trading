from nsepy import get_history
from datetime import date
import pandas as pd


def dump_olhc_for_scrip(scrip):
    data = get_history(symbol=scrip, start=date(2010, 1, 1), end=date.today())
    data.to_csv(f'{scrip}.csv')


def fetch_nifty_50_companies():
    df = pd.read_csv('nifty50.csv');
    return df.iloc[:, 0].to_list()


[dump_olhc_for_scrip(scrip) for scrip in fetch_nifty_50_companies()]
