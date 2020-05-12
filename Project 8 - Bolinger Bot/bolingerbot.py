import pandas as pd
from utility import *
import time

class BolingerBot(object):
    def __init__(self):

        pass

    def start_trading(self, stock, start_date, end_date, window, bolinger_factor, start_balance=100000, start_holding=0):
        balance = start_balance
        holding = start_holding
        value = pd.DataFrame()
        data_range = pd.date_range('2000-01-01', end_date)
        data = get_data([stock], data_range, removeSPY=True)
        transaction_amount = 20
        trading_dates = get_data(
            ["SPY"], pd.date_range(start_date, end_date), removeSPY=False
        ).index


        for date in trading_dates:
            date_range = pd.date_range(start_date, date)
            adj_close = data[date - pd.DateOffset(days=2 * window):date]
            current_price = float(adj_close.iloc[-1])
            rolling_mean = adj_close.iloc[:, 0].rolling(window=window).mean()
            rolling_std = adj_close.iloc[:, 0].rolling(window=window).std()
            factor = float((current_price - rolling_mean[-1]) / (rolling_std[-1]))
            # print(adj_close)

            if factor <= -1 * bolinger_factor:
                balance -= current_price * transaction_amount - (9 * transaction_amount) - (.005 * current_price)
                holding += transaction_amount
                # print(date, "buy", holding)
            elif factor >= bolinger_factor:
                if holding > transaction_amount:
                    balance += current_price * transaction_amount - (9 * transaction_amount) - (.005 * current_price)
                    holding -= transaction_amount
                    # print(date, "sell", holding)

            value = value.append(
                pd.DataFrame({"Value": [current_price * holding + balance]}, index=[date])
            )
        return value