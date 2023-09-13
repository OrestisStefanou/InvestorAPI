import datetime as dt

from app.scripts.scrape_and_store_balance_sheets import fetch_and_store_balance_sheets_for_symbol
from app.scripts.scrape_and_store_cash_flows import fetch_and_store_cash_flows_for_symbol
from app.scripts.scrape_and_store_income_statements import fetch_and_store_income_statements_for_symbol
from app.scripts.scrape_and_store_stock_overview import fetch_and_store_stock_overview_for_symbol
from app.repos.balance_sheet_repo import BalanceSheetRepo


def fetch_and_store_fundamental_data_for_symbol(symbol: str):
    # Check if we already have the latest data for the symbol to avoid extra calls
    balance_sheet_repo = BalanceSheetRepo()

    balance_sheets = balance_sheet_repo.get_balance_sheets_for_symbol(symbol)
    if balance_sheets:
        latest_balance_sheet_date_string = balance_sheets[0].fiscal_date_ending
        latest_balance_sheet_date = dt.datetime.strptime(latest_balance_sheet_date_string, "%Y-%m-%d")
        current_date = dt.datetime.now()
        months_difference = (current_date.year - latest_balance_sheet_date.year) * 12 + (current_date.month - latest_balance_sheet_date.month)
        if months_difference <= 3:
            return
    
    fetch_and_store_balance_sheets_for_symbol(symbol)
    fetch_and_store_cash_flows_for_symbol(symbol)
    fetch_and_store_income_statements_for_symbol(symbol)
    fetch_and_store_stock_overview_for_symbol(symbol)