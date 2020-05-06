import numpy as np
import pandas as pd
import os
import sim_util as util
import datetime as dt
import time


class MarketSim(object):
    def __init__(
        self, portfolio_file, orders_file, start_date, current_date, starting_balance
    ):
        self.balance = starting_balance

        self.start_date = start_date
        self.current_date = current_date

        self.portfolio_file = portfolio_file
        self.orders_file = orders_file

        self.dates = util.get_data(
            ["SPY"], pd.date_range(start_date, "2020-05-01")
        ).index

        try:
            self.current_date_index = self.dates.get_loc(current_date)
        except:
            try:
                self.current_date_index = self.dates.get_loc(
                    dt.datetime.strptime(current_date, "%Y-%m-%d").date()
                    - dt.timedelta(days=1)
                )
            except:
                try:
                    self.current_date_index = self.dates.get_loc(
                        dt.datetime.strptime(current_date, "%Y-%m-%d").date()
                        - dt.timedelta(days=2)
                    )
                except:
                    print("Invalid: Current Date")
        print(self.current_date_index)
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
        # with open(self.orders_file, "w") as f:
        #     f.truncate(0)

        portfolio.to_csv(self.portfolio_file)

    def update(self, time_scale="1d", step_size=1):
        stocklist = []
        self.current_date_index = self.current_date_index + 1
        self.current_date = self.dates[self.current_date_index]

        print(self.current_date, self.current_date_index)
        dates = pd.date_range(self.start_date, self.current_date)

        with open("portfolio.csv", "r") as f:
            portfolio = f.read().splitlines()
            portfolio = [line.split(",") for line in portfolio]

            portfolio.remove(["Symbol", "Stocks"])
            stocklist = [line[0] for line in portfolio]

        return util.get_data(stocklist, dates)
