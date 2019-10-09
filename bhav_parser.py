import pandas as pd
import numpy as np
import datetime as dt
import os


def ohlcConverter(val, defaultValue = np.nan):
    try:
        return float(val)
    except ValueError:
        return defaultValue


def volumeConverter(val, defaultValue = np.nan):
    try:
        return float(val)
    except ValueError:
        return defaultValue



def read_bhav_file(path):
    cols = ['SCRIP', 'DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME', 'INDEXVAR']
    dtypes = {'OPEN': np.float64, 'HIGH': np.float64, 'LOW': np.float64, 'CLOSE': np.float64,
              'VOLUME': np.float64, 'INDEXVAR': np.float64}
    df = pd.read_csv(path, names=cols,
                     dtype=dtypes, converters={'OPEN': ohlcConverter,
                                               'HIGH': ohlcConverter,
                                               'LOW': ohlcConverter,
                                               'CLOSE': ohlcConverter,
                                               'VOLUME': volumeConverter});
    return df

def buildDataFrameForScrip(scrips):
    BHAV_COPY_PATH = 'C:\\Users\\mahad\\Desktop\\algo trading\\bhavcopy\\';
    bhav_files = os.listdir(BHAV_COPY_PATH)
    scrip_map = {scrip: pd.DataFrame(None, None, ['open', 'high', 'low', 'close', 'volume', 'date']) for scrip in scrips}
    for bhav_file in bhav_files:
        df = read_bhav_file(os.path.join(BHAV_COPY_PATH, bhav_file))
        date = dt.datetime.strptime(bhav_file, '%Y-%m-%d-NSE-EQ.txt')
        for scrip in scrips:
            scrip_info = df[df['SCRIP'] == scrip]
            if scrip_info is not None and not scrip_info.empty:
                del scrip_info['DATE']
                del scrip_info['SCRIP']
                del scrip_info['INDEXVAR']
                print(scrip_info)
                scrip_info = scrip_info.iloc[0].to_list()
                scrip_info.append(date)
                df_scrip = scrip_map[scrip]
                df_scrip.loc[len(df_scrip)] = scrip_info
    return scrip_map

def append_roc(df, period = 1):
    df['roc'] = df['close'].pct_change(period)
    return df;
scrip_map = buildDataFrameForScrip(['NSENIFTY', 'GOLDBEES'])
append_roc(scrip_map['NSENIFTY'], 120).to_csv('nsenifty.csv')
append_roc(scrip_map['GOLDBEES'], 120).to_csv('goldbees.csv')

