import asyncio
import time
from typing import List
import pickle

import pandas as pd

from app.scripts.scrape_and_store_fundamental_data import fetch_and_store_fundamental_data_for_symbol
from app.scripts.scrape_and_store_stock_time_series import fetch_and_store_stock_time_series
from app.repos.balance_sheet_repo import BalanceSheetRepo


REQUESTS_PER_MINUTE_LIMIT = 30  # Provider limitation


def get_symbols() -> List[str]:
    """
    Read the symbols from the source csv file
    """
    df = pd.read_csv('app/database/symbols.csv')
    stock_symbols = df['product_id'].to_list()
    return stock_symbols


def update_stock_data():
    api_calls_count = 0
    errored_symbols = ['NESR','BBIG', 'TKO', 'CYXTQ',]

    for symbol in get_symbols():
        if symbol in ['NESR','BBIG', 'TKO', 'CYXTQ',]:
            continue
        
        balance_sheet_repo = BalanceSheetRepo()
        balance_sheets = balance_sheet_repo.get_balance_sheets_for_symbol(symbol)
        if balance_sheets:
            try:
                if asyncio.run(fetch_and_store_stock_time_series(symbol)):
                    api_calls_count += 1
            except Exception:
                pass
            continue


        if api_calls_count + 4 > REQUESTS_PER_MINUTE_LIMIT:
            time.sleep(65)
            api_calls_count = 0

        try:
            if fetch_and_store_fundamental_data_for_symbol(symbol):
                api_calls_count += 4

            if api_calls_count + 1 > REQUESTS_PER_MINUTE_LIMIT:
                time.sleep(65)
                api_calls_count = 0
            
            if asyncio.run(fetch_and_store_stock_time_series(symbol)):
                api_calls_count += 1
        except Exception as err:
            errored_symbols.append(symbol)
            api_calls_count += 1
            print(f'Failed to fetch data for: {symbol} with error : {str(err)}')
    
    with open('errored_symbols.pkl', 'wb') as file:
        pickle.dump(errored_symbols, file)


update_stock_data()
