import asyncio
import time
from typing import List
import pickle

import pandas as pd

from app.scripts.scrape_and_store_fundamental_data import fetch_and_store_fundamental_data_for_symbol
from app.scripts.scrape_and_store_stock_time_series import fetch_and_store_stock_time_series
from app.scripts.scrape_and_store_earnings import fetch_and_store_earnings_for_symbol
from app.dependencies import get_db_conn

REQUESTS_PER_MINUTE_LIMIT = 70  # Provider limitation


def get_symbols() -> List[str]:
    conn = get_db_conn()
    rows = conn.execute("SELECT DISTINCT symbol FROM stocks_with_sector WHERE registered_date='07-06-2024'").fetchall()
    return [
        row[0] for row in rows
    ]


def update_stock_data():
    api_calls_count = 0

    for symbol in get_symbols():
        calls_needed = fetch_and_store_fundamental_data_for_symbol(symbol, dry_run=True)    # Returns the number of calls fetch_and_store_fundamental_data_for_symbol will make without actually making them
        if api_calls_count + calls_needed > REQUESTS_PER_MINUTE_LIMIT:
            time.sleep(65)
            api_calls_count = 0

        try:
            api_calls_made = fetch_and_store_fundamental_data_for_symbol(symbol)
            api_calls_count += api_calls_made

            if api_calls_count + 1 > REQUESTS_PER_MINUTE_LIMIT:
                time.sleep(65)
                api_calls_count = 0
            
            if asyncio.run(fetch_and_store_stock_time_series(symbol)):
                api_calls_count += 1
        except Exception as err:
            api_calls_count += 1    # At least one api call was made in the block above
            print(f'Failed to fetch data for: {symbol} with error : {str(err)}')

update_stock_data()
