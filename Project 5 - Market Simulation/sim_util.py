import pandas as pd

from historical_data import *


def symbol_to_path(symbol):
    """Return CSV file path given ticker symbol.
    If CSV is not already downloaded, will download from yahoo finance """

    base_dir = os.path.dirname(os.getcwd())
    base_dir = os.path.join(base_dir, "data")

    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates, addSPY=True, colname="Adj Close"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    remove_SPY = False
    if addSPY and "SPY" not in symbols:  # add SPY for reference, if absent
        remove_SPY = True
        symbols = ["SPY"] + list(
            symbols
        )  # handles the case where symbols is np array of 'object'

    for symbol in symbols:
        df_temp = pd.read_csv(
            symbol_to_path(symbol),
            index_col="Date",
            parse_dates=True,
            usecols=["Date", colname],
            na_values=["nan"],
        )
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)

        if symbol == "SPY":  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])
        # if remove_SPY:
        #     df.drop("SPY")
    return df
