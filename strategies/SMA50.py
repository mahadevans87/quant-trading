# necessary inports.
from zipline import run_algorithm
from zipline.api import order_target_percent, order_target, symbol, order_target_percent
from datetime import datetime
import pytz
import matplotlib.pyplot as plt  # Set start and end date

start_date = datetime(2015, 1, 1, tzinfo=pytz.UTC)
end_date = datetime(2020, 5, 20, tzinfo=pytz.UTC)


def initialize(context):
    # HDFC Bank. as stock
    context.stock = symbol('TCS')
    context.i = 0


def handle_data(context, data):
    # Skip first 100 days to get full windows
    context.i += 1
    if context.i < 200:
        return  # Compute averages
    # data.history() has to be called with the same params
    # from above and returns a pandas dataframe.
    equity_hist = data.history(context.stock, 'close', bar_count=21, frequency="1d")
    short_mavg = equity_hist.mean()
    long_mavg = data.history(context.stock, 'close', bar_count=50, frequency="1d").mean()
    # Trading logic
    if short_mavg > long_mavg:

        print('Buying - ' + str(context.i) + ', price - ' + str(equity_hist[-1]))
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order_target_percent(context.stock, 1.0)
    elif short_mavg < long_mavg:
        print('Selling - ' + str(context.i) + ', price - ' + str(equity_hist[-1]))
        order_target_percent(context.stock, 0.0)


def analyze(context, perf):
    fig = plt.figure(figsize=(12, 8))

    # First chart
    ax = fig.add_subplot(311)
    ax.set_title('Strategy Results')
    ax.plot(perf['portfolio_value'], linestyle='-',
            label='Equity Curve', linewidth=1.0)
    ax.legend()
    ax.grid(False)

    # Second chart
    ax = fig.add_subplot(312)
    ax.plot(perf['gross_leverage'],
            label='Exposure', linestyle='-', linewidth=1.0)
    ax.legend()
    ax.grid(True)  # Third chart
    ax = fig.add_subplot(313)
    ax.plot(perf['returns'], label='Returns', linestyle='-.', linewidth=1.0)
    ax.legend()
    ax.grid(True)
    plt.savefig('strategy', dpi=400)
    plt.show()


# Fire off the backtest
results = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize,
    analyze=analyze,
    handle_data=handle_data,
    capital_base=10000,
    data_frequency='daily',
    bundle='nse_data'
)
