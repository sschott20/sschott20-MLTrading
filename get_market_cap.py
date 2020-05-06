from yahoofinancials import YahooFinancials

ticker = "AAPL"
yahoo_financials = YahooFinancials(ticker)

balance_sheet_data_qt = yahoo_financials.get_financial_stmts("quarterly", "balance")
income_statement_data_qt = yahoo_financials.get_financial_stmts("quarterly", "income")
all_statement_data_qt = yahoo_financials.get_financial_stmts(
    "quarterly", ["income", "cash", "balance"]
)
apple_earnings_data = yahoo_financials.get_stock_earnings_data()
apple_net_income = yahoo_financials.get_net_income()
