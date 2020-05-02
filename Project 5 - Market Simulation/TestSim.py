
import pandas as pd
import numpy as np
import MarketSim as ms
import sim_util as util
import time

if __name__ == "__main__":
    start_date = "2000-01-24"
    current_date = "2019-02-04"
    portfolio_file = "portfolio.csv"
    orders_file = "orders.csv"

    # start at current date
    Sim = ms.MarketSim(portfolio_file, orders_file, start_date, current_date, 1000000)

    # order stocks
    Sim.order_stonks()

    # compute next day and return df which has current date + 1 days, although not acutally just one day more bcz we skip non trading days
    df = Sim.update()

    # given new knowlage, compute next day of orders rinse + repeat
    # print(df)