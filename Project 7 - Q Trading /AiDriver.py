import qtrader
import pandas as pd
import sys, os
import qutil
import matplotlib
matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
from numpy import average
import time
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
    parameters = {"Adj/SMA": 7, "Bolinger Bands": 7}
    starting_balance = 100000
    start_date = "2012-01-01"
    end_date = "2018-01-01"

    with open('../data/Lists/limited.txt', 'r') as f:
        lines = f.read().splitlines()
    stock_list = lines
    stock_list = ["GOOG"]
    ai_trader = qtrader.QTrader(actions, parameters, start_date, starting_balance)

    times = []
    i = 0
    for stock in stock_list:
        if i > 60:
            break
        t = time.time()
        print(i,' : ', stock)
        try:
            ai_trader.train(stock, start_date, end_date)
        except Exception as e:
            print(e)
            print("--ERROR--")
        times.append(time.time() - t)
        i += 1
    ai_trader.output_table()

    df = qutil.get_data(['GOOG'], pd.date_range(start_date, end_date))
    qutil.plot_data(df / df.values[0])
    ai_trader.train('GOOG', '2018-01-01', '2019-01-01')
    ai_trader.plot_port_value(normalized=True)


    print(f'--- Total training time : {round(sum(times), 2)} ---')
    print(f'--- Average per training session : {round(average(times), 2)} ---')
    plt.show()





