import pandas as pd
import scipy.optimize as spo
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import os
import sys

sys.path.insert(0, os.path.dirname(os.getcwd()))
from util import get_data, plot_data


def portfolio_statistics(normed, allocs, start_value):
    # Function to be minimized

    alloced = normed * allocs
    position_value = alloced * start_value
    portfolio_value = position_value.sum(axis=1)
    daily_returns = (portfolio_value[1:] / portfolio_value.values[:-1]) - 1
    risk = daily_returns.std()
    cumulative_return = -(portfolio_value[-1] / portfolio_value.values[0]) - 1
    sharpe_ratio = (daily_returns - 0.0).mean() / risk
    return sharpe_ratio * -1


def optimize_portfolio(
    start_date, end_date, symbols, gen_plot, start_value,
):

    risk_free_rate = 0.0

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(symbols, dates)

    prices_stocks = prices_all.copy()
    prices_stocks = prices_stocks[symbols]

    prices_stocks.fillna(method="ffill", inplace=True)
    prices_stocks.fillna(method="bfill", inplace=True)

    prices_SPY = prices_all.copy()
    prices_SPY = prices_SPY["SPY"]

    # Find allocations with optimization
    n = len(symbols)
    normed = prices_stocks / prices_stocks.values[0]
    guess = [1.0 / n] * n

    bounds = [(0.0, 1.0) for i in normed.columns]
    constraints = {"type": "eq", "fun": lambda inputs: 1.0 - np.sum(inputs)}
    print("about to minimize")
    minimize_result = spo.minimize(
        portfolio_statistics,
        guess,
        args=(normed, start_value),
        method="SLSQP",
        constraints=constraints,
        bounds=bounds,
    )
    allocs = minimize_result.x

    # Calculate portfolio statistics
    alloced = normed * allocs
    position_value = alloced * start_value
    portfolio_value = position_value.sum(axis=1)
    daily_returns = (portfolio_value[1:] / portfolio_value.values[:-1]) - 1
    cumulative_return = (portfolio_value[-1] / portfolio_value.values[0]) - 1
    avg_daily_return = daily_returns.mean()
    daily_return_std = daily_returns.std()
    sharpe_ratio = (daily_returns - risk_free_rate).mean() / daily_return_std

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        plot_data(normed, title="Normalized Stock Prices")
        prices_SPY = prices_SPY / prices_SPY.values[0]
        portfolio_value = portfolio_value / portfolio_value.values[0]
        df_temp = pd.concat(
            [portfolio_value, prices_SPY], keys=["Portfolio", "SPY"], axis=1
        )
        plot_data(df_temp, title="Sharpe-optimized portfolio and SPY performance")
    return allocs, cumulative_return, avg_daily_return, daily_return_std, sharpe_ratio


def optimization_driver():
    # Portfolio parameters
    start_date = dt.datetime(2019, 1, 1)
    end_date = dt.datetime(2020, 1, 1)
    # symbols = ["GOOG", "AAPL", "UAL", "XOM", "ZM", "GLD", "TSLA"]
    symbols = []

    # ALLLLLL THE STOOOOCKSSS
    with open("../data/Lists/sp5002020.txt", "r") as file:
        for line in file:
            symbols.append(line.strip())
    gen_plots = False
    start_value = 1000
    # Assess the portfolio
    (
        allocations,
        cumulative_return,
        avg_daily_return,
        daily_return_std,
        sharpe_ratio,
    ) = optimize_portfolio(
        start_date=start_date,
        end_date=end_date,
        symbols=symbols,
        gen_plot=gen_plots,
        start_value=start_value,
    )
    # for ease of viewing
    allocations = allocations.round(4)

    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print("\n")
    print("--- Allocations --- ")
    for i in range(len(symbols)):
        if allocations[i] != 0:
            print(f"{symbols[i]} : {allocations[i]}")
    print("\n")
    print(f"Sharpe Ratio: {sharpe_ratio}")
    print(f"Volatility (stdev of daily returns): {daily_return_std}")
    print(f"Average Daily Return: {avg_daily_return}")
    print(f"Cumulative Return: {cumulative_return}")
    print(f"\n--- FINAL PROFIT ---\n ${round(cumulative_return * start_value, 2)}")
    plt.show()


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    optimization_driver()
