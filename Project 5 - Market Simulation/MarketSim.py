import numpy as np



class MarketSim(object):

    def __init__(self, portfolio_file, orders_file, start_date):
        self.date = start_date
        self.portfolio_file = portfolio_file
        self.orders_file = orders_file

        self.orders = []
        self.portfolio = []

        self.update_files()

    def update_files(self):
        with open(self.portfolio_file) as f:
            self.portfolio = f.readlines()[1:]
            self.portfolio = [a.strip("\n") for a in self.portfolio]
        with open(self.orders_file) as f:
            self.orders = f.readlines()[1:]
            self.orders = [a.strip("\n") for a in self.orders]

    def order(self):
        self.update_files()

        print(self.portfolio)
        print(self.orders)
        # for transaction in self.orders:



    def end_day(self):

        pass

