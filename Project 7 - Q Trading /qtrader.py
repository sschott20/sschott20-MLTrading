import pandas as pd
import numpy as np
from historical_data import *
import qutil
import qlearn_trading as qlearn
import math


class QTrader(object):

    def __init__(self, actions, parameters, start_date, starting_money=100000):
        self.actions = actions
        self.balance = starting_money
        self.parameters = parameters
        self.start_date = start_date
        self.holding = 2
        self.trading_dates = qutil.get_data(["SPY"], pd.date_range(start_date, '2020-05-01'), removeSPY=False).index

        self.ai = qlearn.QLearn(actions, q=None, c=0.2, alpha=0.2, gamma=0.9, cdecay=0.999)

    def calculate_state_value(self, stock):
        """
        range should be from start of data to latest date that the ai is allowed to see
        """
        date_range = pd.date_range("2000-01-01"., "2020-05-03")
        adj_close = qutil.get_data(stock, date_range, removeSPY=True)
        state = []

        if "Adj/SMA" in self.parameters:
            window = self.parameters["Adj/SMA"]
            sma = adj_close.iloc[:, 0].rolling(window=window).mean()
            adj = adj_close.iloc[:, 0]
            sma_adj = (sma / adj).dropna()
            steps = 50
            stepsize = math.floor(len(sma_adj) / steps)

            thresholds = []
            sma_adj = sma_adj.sort_values(0)
            thresholds.append(0)
            for i in range(0, steps):
                thresholds.append(round(sma_adj.iloc[(i + 1) * stepsize], 4))
            thresholds.append(10)

            discritized = pd.cut(sma_adj, bins=thresholds, labels=[x for x in range(steps + 1)])

            x = discritized[date_range].dropna()

            state.append(x[-1])

        if "Holding" in self.parameters:
            state.append(self.holding)
        q = []
        for j in state:
            q.append("{0:0=2d}".format(j))
        print(q)
        state_int = int("".join(q))

        return state_int

    def train(self, stock, start_date):
        last_action = None
        last_state = None
        current_date = start_date

        # print(start_index)
        for date in self.trading_dates:
            print(date)
            pass
            # state = self.calculate_state_value(stock, date_range=pd.date_range('2000-01-01', date))
