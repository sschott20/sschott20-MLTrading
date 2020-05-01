
import pandas as pd
import numpy as np
import MarketSim as ms

if __name__ == "__main__":
    start_date = "2019-01-24"
    current_date = "2019-02-02"
    portfolio_file = "portfolio.csv"
    orders_file = "orders.csv"

    Sim = ms.MarketSim(portfolio_file, orders_file, start_date, current_date)
    Sim.order_stonks()
    df = Sim.update()
    # print(df)