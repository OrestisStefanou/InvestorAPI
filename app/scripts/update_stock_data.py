import asyncio
import time
from typing import List

from app.scripts.scrape_and_store_fundamental_data import fetch_and_store_fundamental_data_for_symbol
from app.scripts.scrape_and_store_stock_time_series import fetch_and_store_stock_time_series


def get_symbols() -> List[str]:
    """
    Modify this function logic to get the symbols from ibd data tables
    """
    return [
        'MITK',
        'IR',
        'TT',
        'PINS',
        'NVT',
        'TEX',
        'ORCL',
        'PWR',
        'LLY',
        'HAL',
        'FLS',
        'FMX',
        'FTI',
        'OII',
        'FRSH',
        'MDB',
        'NCNO',
        'OTEX',
        'CEIX',
        'AROC',
    ]


for symbol in get_symbols():
    print("Fetching data for:", symbol)
    fetch_and_store_fundamental_data_for_symbol(symbol)
    asyncio.run(fetch_and_store_stock_time_series(symbol))
    time.sleep(65)
