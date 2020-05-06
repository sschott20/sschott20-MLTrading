import qtrader
import pandas as pd

if __name__ == "__main__":
    print("START")
    actions = ["BUY-1", "BUY-5", "SELL-1", "SELL-5", "NOTHING"]
    parameters = {"Adj/SMA": 7, "Holding": 0}
    starting_balance = 100000
    t = "2000-01-01"
    start_date = "2020-01-04"

    range = pd.date_range(start_date, "2011-01-01")
    stock = ["GOOG"]

    ai_trader = qtrader.QTrader(actions, parameters, start_date, starting_balance)
    # ai_trader.calculate_state_value(stock, range)
    ai_trader.train(stock, start_date)
