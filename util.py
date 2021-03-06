import pandas as pd

from historical_data import *


def symbol_to_path(symbol, base_dir=None):
    """Return CSV file path given ticker symbol.
    If CSV is not already downloaded, will download from yahoo finance """
    if base_dir == None:
        base_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(base_dir, "MLTrading-Solo/ALL_DATA/data")

    if not os.path.exists(os.path.join(base_dir, "{}.csv".format(str(symbol)))):
        pull_specific_stocks([symbol])

    return os.path.join(base_dir, "{}.csv".format(str(symbol)))
    # if base_dir is None:
    #     base_dir = os.environ.get("MARKET_DATA_DIR", "../data/")
    #     print(base_dir)
    # return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def symbol_to_check_path(symbol, base_dir=None):
    """Return CSV file path given ticker symbol.
    If CSV is not already downloaded, will download from yahoo finance """
    if base_dir == None:
        base_dir = os.path.dirname(os.getcwd())
        base_dir = os.path.join(base_dir, "MLTrading-Solo/ALL_DATA/Check_data")

    return os.path.join(base_dir, "c{}.csv".format(str(symbol)))
    # if base_dir is None:
    #     base_dir = os.environ.get("MARKET_DATA_DIR", "../data/")
    #     print(base_dir)
    # return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def symbol_to_old_path(symbol, base_dir=None):
    """Return CSV file path given ticker symbol."""
    if base_dir is None:
        base_dir = os.environ.get("MARKET_DATA_DIR", "../old_data/")
    print(base_dir)
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_check_data(symbols, dates, addSPY=True, colname="PX_LAST"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and "SPY" not in symbols:  # add SPY for reference, if absent
        symbols = ["SPY"] + list(
            symbols
        )  # handles the case where symbols is np array of 'object'

    for symbol in symbols:
        df_temp = pd.read_csv(
            symbol_to_check_path(symbol),
            index_col="date",
            parse_dates=True,
            usecols=["date", colname],
            na_values=["nan"],
        )
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)

        if symbol == "SPY":  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def get_data(symbols, dates, addSPY=True, colname="Adj Close"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and "SPY" not in symbols:  # add SPY for reference, if absent
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

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    import matplotlib.pyplot as plt

    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # plt.show()


def get_orders_data_file(basefilename):
    return open(
        os.path.join(os.environ.get("ORDERS_DATA_DIR", "orders/"), basefilename)
    )


def get_learner_data_file(basefilename):
    return open(
        os.path.join(os.environ.get("LEARNER_DATA_DIR", "Data/"), basefilename), "r"
    )


def get_robot_world_file(basefilename):
    return open(
        os.path.join(os.environ.get("ROBOT_WORLDS_DIR", "testworlds/"), basefilename)
    )
