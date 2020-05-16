import sys
from utility import *
import matplotlib

matplotlib.use("TKAgg")
from matplotlib import pyplot as plt
import bolingerbot as bb
import time
from numpy import average


def blockPrint():
    sys.stdout = open(os.devnull, "w")


# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    print("START")
    start_balance = 100000
    start_date = "2015-01-01"
    end_date = "2020-01-01"
    # bolinger_factor = 2
    # window = 20
    # with open('../data/Lists/limited.txt', 'r') as f:
    #     lines = f.read().splitlines()
    # BEST window : 45 Factor 1
    stock_list = ["PNR", "GOOG", "AAPL", "XOM", "ABC", "ATO", "C", "CAH", "DAL"]
    trader = bb.BolingerBot()
    times = []
    window = 20
    bolinger_factor = 2.2

    for stock in stock_list:
        t = time.time()
        print(stock, window, bolinger_factor)
        value = trader.start_trading(
            stock,
            start_date=start_date,
            end_date=end_date,
            window=window,
            bolinger_factor=bolinger_factor,
            start_balance=start_balance,
            start_holding=0,
        )

        data = get_data([stock], pd.date_range(start_date, end_date))

        sma = data.rolling(window=window).mean()
        std = data.rolling(window=window).std()

        ax = data[stock].plot(title=stock)
        upper_bound = sma + bolinger_factor * std
        lower_bound = sma - bolinger_factor * std
        upper_bound.plot(label="upper", ax=ax)
        lower_bound.plot(label="lower", ax=ax)

        with open(f"return_output/return-{stock}.txt", "a") as f:
            s = str(window) + " " + str(bolinger_factor)
            f.write(s)

            s = " Bot return : " + str(
                round(((float(value.iloc[-1]) - start_balance) / start_balance) + 1, 3)
            )
            f.write(s)

            s = " Stock Return : " + str(
                round(float(data.iloc[-1]) / float(data.iloc[0]), 3)
            )
            f.write(s)
            f.write("\n")

        times.append(time.time() - t)

        plot_data(value)

        plt.show()

    print(f"--- Total training time : {round(sum(times)/60, 2)} ---")
    print(f"--- Average per training session : {round(average(times)/60, 2)} ---")
