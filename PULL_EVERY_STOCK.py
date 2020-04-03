import math
import os
import shutil
import time
import urllib.request
import time
import pandas as pd

# period1 and period2 are Unix time stamps for your start and end date
# interval is the data retrieval interval (this can be either 1d, 1w or 1m)

# NEED RETURN AND OUTSTANDING NUMBER OF SHARES


def pull_all_data(src, start_idx=0):
    print("PULLING DATA FROM: " + src)
    with open(src, "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        for i in range(start_idx, file_length):
            company = file_lines[i].strip()
            ticker = company.split()
            # print(ticker[0])
            pull_specific_stocks([ticker[0]])


def pull_specific_stocks(stocks):
    """Download data of specific stocks from yahoo finance"""
    for stock in stocks:
        print("Downloading historical data for: " + stock)
        pull_historical_data(stock)


current_time = str(math.floor(time.time()))
# Times:
# 2019-01-01 : 1546300800
# 2000-01-01 : 946684800


def make_url(
    ticker_symbol, period1="1546300800", period2=current_time, interval="1d",
):
    return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events=history".format(
        ticker_symbol, period1, period2, interval
    )


def make_filename(ticker_symbol):
    return ticker_symbol + ".csv"


def pull_historical_data(ticker_symbol):
    filename = make_filename(ticker_symbol)
    try:
        urllib.request.urlretrieve(make_url(ticker_symbol), filename)

        df = pd.read_csv(
            filename,
            index_col="Date",
            parse_dates=True,
            # usecols=["Date", "Adj Close"],
            na_values=["nan"],
        )
        df_temp = df.copy()
        df_temp = df_temp["Adj Close"]

        df_temp = df_temp.rename(columns={"Adj Close": "Daily Return"})
        df_add = (df_temp[1:] / df_temp.values[:-1]) - 1
        # print(df_add)
        # df.join(df_add)
        df["Daily Return"] = df_add

        dst = os.getcwd() + "/ALL_DATA/Data"

        df.to_csv(os.path.join(dst, filename), index="Date")
        os.remove(filename)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    # start_time = time.time()

    # pull_all_data("ALL_DATA/Lists/NASDAQ.txt")
    pull_all_data("ALL_DATA/Lists/ALL_SYMBOLS_TEST.txt")
    # print(time.time()-start_time)
    # stocks = ['BRK-B']
    # pull_specific_stocks(stocks)
