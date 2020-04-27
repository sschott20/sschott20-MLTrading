
import pandas as pd
import numpy as np
import MarketSim as ms
if __name__ == "__main__":

    current_date = "2019-01-01"
    portfolio_file = "portfolio.csv"
    orders_file = "orders.csv"

    Sim = ms.MarketSim(portfolio_file, orders_file, "2019-01-01")
    Sim.order()
