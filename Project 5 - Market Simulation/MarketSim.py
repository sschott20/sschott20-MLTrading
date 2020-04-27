import numpy as np
import pandas as pd
import os

class MarketSim(object):

    def __init__(self, portfolio_file, orders_file, start_date):
        self.date = start_date
        self.portfolio_file = portfolio_file
        self.orders_file = orders_file

        self.update_files()

    def update_files(self):
        # self.portfolio = np.genfromtxt(self.portfolio_file,delimiter=",")
        # self.orders = np.genfromtxt(self.orders_file,delimiter=",")
        self.portfolio = pd.read_csv(self.portfolio_file)
        self.orders = pd.read_csv(self.orders_file)

    def order_stonks(self):
        self.update_files()

        t = [self.portfolio, self.orders]
        portfolio = pd.concat(t, ignore_index=True)

        portfolio = portfolio.groupby("Symbol", axis=0).sum()

        os.remove(self.portfolio_file)
        with open(self.orders_file, "w") as f:
            f.truncate(0)

        portfolio.to_csv(self.portfolio_file)

    def end_day(self):
        pass
