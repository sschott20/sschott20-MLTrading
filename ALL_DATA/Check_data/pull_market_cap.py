from __future__ import print_function
import time
import intrinio_sdk
from intrinio_sdk.rest import ApiException
from pprint import pprint

intrinio_sdk.ApiClient().configuration.api_key[
    "api_key"
] = "OjQ5OGM2ZDBlODZhYjg1OTdiZmIzNmIzYjNkNzgxMmU4"

security_api = intrinio_sdk.SecurityApi()

identifier = (
    "AAPL"  # str | A Security identifier (Ticker, FIGI, ISIN, CUSIP, Intrinio ID)
)
start_date = "2019-01-02"  # date | Return intraday prices starting at the specified date (optional)
end_date = "2019-01-04"  # date | Return intraday prices stopping at the specified date (optional)

try:
    api_response = security_api.get_security_intraday_prices(
        identifier, start_date=start_date, end_date=end_date
    )
    print(api_response.intraday_prices)
except ApiException as e:
    print("Exception when calling SecurityApi->get_security_intraday_prices: %s\n" % e)
