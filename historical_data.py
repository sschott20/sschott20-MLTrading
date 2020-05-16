import math
import os
import shutil
import time
import urllib.request
import time

# period1 and period2 are Unix time stamps for your start and end date
# interval is the data retrieval interval (this can be either 1d, 1w or 1m)

def pull_all_data(src, start_idx=0):
    print("PULLING DATA FROM: " + src)
    with open(src, "r") as file:
        file_lines = file.readlines()
        file_length = len(file_lines)
        for i in range(start_idx, file_length):
            company = file_lines[i].strip()
            ticker = company.split()
            pull_specific_stocks([ticker[0]])

def pull_specific_stocks(stocks):
    """Download data of specific stocks from yahoo finance"""
    for stock in stocks:
        print("Downloading historical data for: " + stock)

        pull_historical_data(stock)

        try:
            filename = make_filename((stock))
            src = os.getcwd()
            dst = src + "/Data/"
            shutil.move(os.path.join(src, filename), os.path.join(dst, filename))
        except Exception as e:
            with open("Data/Lists/missed.txt", "a") as file:
                file.write(stock)
                file.write("\n")
                file.close()
            print(e)
current_time = str(math.floor(time.time()))

# Times:
# 2019-01-01 : 1546300800
# 2000-01-01 : 946684800
def make_url(
    ticker_symbol, period1="946684800", period2=current_time, interval="1d",
):
    return "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval={}&events=history".format(
        ticker_symbol, period1, period2, interval
    )


def make_filename(ticker_symbol):
    return ticker_symbol + ".csv"


def pull_historical_data(ticker_symbol):
    try:
        urllib.request.urlretrieve(
            make_url(ticker_symbol), make_filename(ticker_symbol)
        )
    except Exception as e:
        print(e)
        print("Error Fetching stock, may not exist")


if __name__ == "__main__":
    # start_time = time.time()

    # pull_all_data("ALL_DATA/Lists/NASDAQ.txt")
    pull_all_data("ALL_DATA/Lists/ALL_SYMBOLS_TEST.txt")
    # print(time.time()-start_time)
    # stocks = ['BRK-B']
    # pull_specific_stocks(stocks)
