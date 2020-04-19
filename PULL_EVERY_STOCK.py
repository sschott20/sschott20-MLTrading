import math
import os
import urllib.request
from urllib.error import HTTPError
import time
import pandas as pd

# interval is the data retrieval interval (this can be either 1d, 1w or 1m)

# OUTSTANDING NUMBER OF SHARES


def pull_all_data(src, start_idx=0):
    file_length = 0

    with open("ALL_DATA/Lists/missed.txt", "a") as missed_file:
        missed_file.truncate(0)
        missed_file.close()

    print("PULLING DATA FROM: " + src)

    with open(src, "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)

        for i in range(start_idx, file_length):
            symbol = file_lines[i].strip()
            screen = True
            while screen:
                try:
                    print("Downloading historical data for: " + symbol)
                    pull_historical_data(symbol)
                    screen = False
                except HTTPError as e:
                    if e.code == 401:
                        print(f"\nWaiting 30 Seconds, index = {i}")
                        time.sleep(30)
                    else:
                        print(e)
                        with open("ALL_DATA/Lists/missed.txt", "a") as missed_file:
                            missed_file.write(symbol)
                            missed_file.write("\n")
                            missed_file.close()
                        screen = False

    return file_length


current_time = str(math.floor(time.time()))
# Times:
# 2020-03-19 : 1584576000
# 2020-01-01 : 1577836800
# 2019-01-01 : 1546300800
# 2000-01-01 : 946684800
#


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

    urllib.request.urlretrieve(
        make_url(ticker_symbol), os.path.join(os.getcwd(), filename)
    )

    df = pd.read_csv(filename, index_col="Date", parse_dates=True, na_values=["nan"],)
    df_temp = df.copy()
    df_temp = df_temp["Adj Close"]

    df_temp = df_temp.rename(columns={"Adj Close": "Daily Return"})
    df_add = (df_temp[1:] / df_temp.values[:-1]) - 1

    df["Daily Return"] = df_add

    dst = os.getcwd() + "/ALL_DATA/Data"

    df.to_csv(os.path.join(dst, filename), index="Date")
    os.remove(filename)


def get_PRN_data():
    urllib.request.urlretrieve(
        f"https://query1.finance.yahoo.com/v7/finance/download/PRN?period1=1546300800&period2={current_time}&interval=1d&events=history",
        "ALL_DATA/Data/_PRN.csv",
    )
    df = pd.read_csv(
        "ALL_DATA/Data/_PRN.csv", index_col="Date", parse_dates=True, na_values=["nan"],
    )
    df_temp = df.copy()
    df_temp = df_temp["Adj Close"]

    df_temp = df_temp.rename(columns={"Adj Close": "Daily Return"})
    df_add = (df_temp[1:] / df_temp.values[:-1]) - 1

    df["Daily Return"] = df_add

    dst = os.getcwd() + "/ALL_DATA/Data"

    df.to_csv(os.path.join(dst, "_PRN.csv"), index="Date")


if __name__ == "__main__":

    start_time = time.time()
    get_PRN_data()
    indices = pull_all_data("ALL_DATA/Lists/indices.txt")
    stop_index = pull_all_data("ALL_DATA/Lists/COMPANY_LIST.txt")

    end_time = time.time()

    print("\n--- TOTAL TIME ---")
    print(f"{round(end_time-start_time, 4)} seconds\n")
    print(f"--- AVERAGE TIME OVER {stop_index + indices} STOCKS ---")
    print(f"{round((end_time - start_time) / (stop_index + indices) , 4)} SECONDS PER STOCK")
