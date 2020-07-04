import csv

import pandas as pd
import os, glob
import numpy as np


def read_nifty_constituents():
    nifty_dir = 'C:\\Users\\msreeni\\wkspc\\personal\\quant-trading\\index_constituents\\nifty_constituents'
    start_year = 2011  # 2011
    end_year = 2020  # 2020
    years = np.arange(start_year, end_year + 1)
    result_df = pd.DataFrame(columns=['date', 'tickers'])
    for year in years:
        year_dir = os.path.join(nifty_dir, str(year))
        os.chdir(year_dir)
        stocks_for_year = []
        for csv_file in glob.glob('*.csv'):
            print('Parsing - ' + csv_file)
            df = pd.read_csv(os.path.join(year_dir, csv_file), skiprows=2)
            stocks_for_year.extend(list(df.dropna().iloc[:, 1]))
        stock_string = ','.join(stocks_for_year)
        row = [str(year) + '-' + '06-01', stock_string]
        print(row)
        result_df.loc[len(result_df)] = row
    return result_df

nifty_const_df = read_nifty_constituents()
nifty_const_df.to_csv('C:\\Users\\msreeni\\wkspc\\personal\\quant-trading\\index_constituents\\nifty_constituents.csv', index=False)
