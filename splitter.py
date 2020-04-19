lines_per_file = 317
smallfile = None
counter = 0
with open('ALL_DATA/Lists/Bloomberg_final (1).csv') as bigfile:
    for lineno, line in enumerate(bigfile):
        if lineno % lines_per_file == 0:
            if smallfile:
                smallfile.close()
            line_split = line.split(",")
            symbol = line_split[1]

            with open("ALL_DATA/Lists/COMPANY_LIST.txt", "a") as file:
                file.write(symbol + "\n")

            small_filename = 'c{}.csv'.format(symbol)
            smallfile = open("ALL_DATA/Check_data/" + small_filename, "w")
            smallfile.write("market,symbol,company_name,CUSIP,hq_location,date,BEST_EPS,BS_SH_OUT,HISTORICAL_MARKET_CAP,PX_LAST,PX_VOLUME,TOT_RETURN,TRAIL_12M_EPS")
        smallfile.write(line)
    if smallfile:
        smallfile.close()