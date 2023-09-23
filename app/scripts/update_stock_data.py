import asyncio
import time
from typing import List

import pandas as pd

from app.scripts.scrape_and_store_fundamental_data import fetch_and_store_fundamental_data_for_symbol
from app.scripts.scrape_and_store_stock_time_series import fetch_and_store_stock_time_series


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
    for symbol in get_symbols():
        if api_calls_count + 4 > 30:
            time.sleep(65)
            api_calls_count = 0

        if fetch_and_store_fundamental_data_for_symbol(symbol):
            api_calls_count += 4

        if api_calls_count + 1 > 30:
            time.sleep(65)
            api_calls_count = 0
        
        if asyncio.run(fetch_and_store_stock_time_series(symbol)):
            api_calls_count += 1


update_stock_data()
