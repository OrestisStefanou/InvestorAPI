import asyncio
import time
from typing import List
import pickle

import pandas as pd

from app.scripts.scrape_and_store_fundamental_data import fetch_and_store_fundamental_data_for_symbol
from app.scripts.scrape_and_store_stock_time_series import fetch_and_store_stock_time_series


REQUESTS_PER_MINUTE_LIMIT = 30  # Provider limitation


def get_symbols() -> List[str]:
    """
    Read the symbols from the source csv file
    """
    # df = pd.read_csv('app/database/symbols.csv')
    # stock_symbols = df['product_id'].to_list()
    # return stock_symbols
    from app.dependencies import get_db_conn
    conn = get_db_conn()
    rows = conn.execute("SELECT DISTINCT symbol FROM balance_sheet").fetchall()
    return [
        row[0] for row in rows
    ]


def update_stock_data():
    api_calls_count = 0
    # with open('errored_symbols.pkl', 'rb') as file:
    #     errored_symbols = pickle.load(file)


    for symbol in get_symbols():
        # if symbol in errored_symbols:
        #     continue
        
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
