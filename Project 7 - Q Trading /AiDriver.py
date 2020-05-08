import qtrader
import pandas as pd
import sys, os
import qutil
import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    print("START")
    actions = ["NNN"]
    for i in range(1, 3):
        actions.append(f"S{i * 25}")
        actions.append(f"B{i * 25}")
    parameters = {"Adj/SMA": 7, "Holding": 0, "Daily Return": 0, "Balance": 0}
    starting_balance = 100000
    start_date = "2018-01-01"
    end_date = "2020-05-01"
    # stock_list = ["GOOG", "TSLA", "AAPL", "AA", "A"]
    stock_list = ['GOOG']
    ai_trader = qtrader.QTrader(actions, parameters, start_date, starting_balance)


    for i in range(10):
        ai_trader.train(stock_list[0], start_date, end_date)

    df = qutil.get_data(stock_list, pd.date_range(start_date, end_date))
    qutil.plot_data(df/df.values[0])
    ai_trader.plot_port_value()
    ai_trader.output_table()
    plt.show()





