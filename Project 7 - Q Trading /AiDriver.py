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
    actions = ["SAX", "NNX"]
    for i in range(1, 3):
        actions.append(f"S{i * 25}")
        actions.append(f"B{i * 25}")
    parameters = {"Adj/SMA": 7, "Holding": 0, "Daily Return": 0, "Balance": 0}
    starting_balance = 100000
    start_date = "2016-01-01"
    end_date = "2020-01-01"
    stock_list = ["GOOG", "TSLA", "AAPL", "AA", "A"]

    ai_trader = qtrader.QTrader(actions, parameters, start_date, starting_balance)
    # for stock in stock_list:
    #     print(stock)
    #     ai_trader.train(stock, start_date)
    # blockPrint()

    for i in range(1):
        ai_trader.train("NVDA", start_date, end_date)
    # enablePrint()
    # ai_trader.train("GOOG", start_date)
    ai_trader.output_table()
    df = qutil.get_data(["NVDA"], pd.date_range(start_date, end_date))
    qutil.plot_data(df/df.values[0])
    ai_trader.plot_port_value()
    plt.show()



