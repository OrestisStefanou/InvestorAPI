import datetime as dt

from app.scripts.scrape_and_store_balance_sheets import fetch_and_store_balance_sheets_for_symbol
from app.scripts.scrape_and_store_cash_flows import fetch_and_store_cash_flows_for_symbol
from app.scripts.scrape_and_store_income_statements import fetch_and_store_income_statements_for_symbol
from app.scripts.scrape_and_store_stock_overview import fetch_and_store_stock_overview_for_symbol
from app.repos.balance_sheet_repo import BalanceSheetRepo
from app.repos.cash_flow_repo import CashFlowRepo
from app.repos.income_statement_repo import IncomeStatementRepo
from app.repos.stock_overview_repo import StockOverviewRepo


def _have_latest_balance_sheets(symbol: str, balance_sheet_repo: BalanceSheetRepo) -> bool:
    balance_sheets = balance_sheet_repo.get_balance_sheets_for_symbol(symbol)
    if balance_sheets:
        latest_balance_sheet_date_string = balance_sheets[0].fiscal_date_ending
        latest_balance_sheet_date = dt.datetime.strptime(latest_balance_sheet_date_string, "%Y-%m-%d")
        current_date = dt.datetime.now()
        months_difference = (current_date.year - latest_balance_sheet_date.year) * 12 + (current_date.month - latest_balance_sheet_date.month)
        if months_difference <= 3:
            return True
    
    return False


def _have_latest_cash_flow(symbol: str, cash_flow_repo: CashFlowRepo) -> bool:
    cash_flows = cash_flow_repo.get_cash_flows_for_symbol(symbol)
    if cash_flows:
        latest_cash_flow_date_string = cash_flows[0].fiscal_date_ending
        latest_cash_flow_date = dt.datetime.strptime(latest_cash_flow_date_string, "%Y-%m-%d")
        current_date = dt.datetime.now()
        months_difference = (current_date.year - latest_cash_flow_date.year) * 12 + (current_date.month - latest_cash_flow_date.month)
        if months_difference <= 3:
            return True
    
    return False


def _have_latest_income_statements(symbol: str, income_statement_repo: IncomeStatementRepo) -> bool:
    income_statements = income_statement_repo.get_income_statements_for_symbol(symbol)
    if income_statements:
        latest_income_statement_date_string = income_statements[0].fiscal_date_ending
        latest_income_statement_date = dt.datetime.strptime(latest_income_statement_date_string, "%Y-%m-%d")
        current_date = dt.datetime.now()
        months_difference = (current_date.year - latest_income_statement_date.year) * 12 + (current_date.month - latest_income_statement_date.month)
        if months_difference <= 3:
            return True
    
    return False


def _have_latest_stock_overview(symbol: str, stock_overview_repo: StockOverviewRepo) -> bool:
    stock_overview_latest_date = stock_overview_repo.get_latest_registered_datetime_for_symbol(symbol)
    if stock_overview_latest_date:
        current_date = dt.datetime.now()
        months_difference = (current_date.year - stock_overview_latest_date.year) * 12 + (current_date.month - stock_overview_latest_date.month)
        if months_difference <= 1:
            return True
    
    return False


def fetch_and_store_fundamental_data_for_symbol(symbol: str, dry_run: bool = False) -> int:
    """
    Funtion that makes 4 separate calls to our provider:
    1. Fetch balance sheets
    2. Fetch cash flows
    3. Fetch income statements
    4. Fetch company overview

    We then store these data on our side.
    In case we already have the latest data on our side we don't perform
    any unnecessary calls.
    Returns the numbers of api calls that were made.
    If dry_run=True no api calls are made, we just return the number of calls that would be made
    """
    # Check if we already have the latest data for the symbol to avoid extra calls
    api_calls_count = 0
    balance_sheet_repo = BalanceSheetRepo()
    cash_flow_repo = CashFlowRepo()
    income_statement_repo = IncomeStatementRepo()
    stock_overview_repo = StockOverviewRepo()

    if _have_latest_balance_sheets(symbol, balance_sheet_repo) is False:
        print("Fetching balance sheets for symbol:", symbol)
        if dry_run is False:
            fetch_and_store_balance_sheets_for_symbol(symbol)
        api_calls_count += 1
    
    if _have_latest_cash_flow(symbol, cash_flow_repo) is False:
        print("Fetching cash flows for symbol:", symbol)
        if dry_run is False:
            fetch_and_store_cash_flows_for_symbol(symbol)
        api_calls_count += 1
    
    if _have_latest_income_statements(symbol, income_statement_repo) is False:
        print("Fetching income statements for symbol:", symbol)
        if dry_run is False:
            fetch_and_store_income_statements_for_symbol(symbol)
        api_calls_count += 1
    
    if _have_latest_stock_overview(symbol, stock_overview_repo) is False:
        print("Fetching stock overview for symbol:", symbol)
        if dry_run is False:
            fetch_and_store_stock_overview_for_symbol(symbol)
        api_calls_count += 1
    
    return api_calls_count
