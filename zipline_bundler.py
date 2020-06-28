import pandas as pd
import os


def generate_zipline_csv(input_csv, output_dir, output_file):
    input_df = pd.read_csv(input_csv)
    output_df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume', 'dividend', 'split'])
    output_df['date'] = input_df['Date'];
    output_df['open'] = input_df['Open'];
    output_df['high'] = input_df['High'];
    output_df['low'] = input_df['Low'];
    output_df['close'] = input_df['Close'];
    output_df['volume'] = input_df['Volume'];
    output_df['dividend'] = 0.0;
    output_df['split'] = 1.0;
    print(output_df.head())
    # Create output directory if not exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_df.to_csv(os.path.join(output_dir, output_file), index=False)


[generate_zipline_csv(os.path.join('nifty50_olhc', filename), 'zipline_bundle', filename) for filename in
 os.listdir('nifty50_olhc')]

# generate_zipline_csv('nifty50_olhc\\ADANIPORTS.csv', 'zipline_bundle', 'ADANIPORTS.csv')
