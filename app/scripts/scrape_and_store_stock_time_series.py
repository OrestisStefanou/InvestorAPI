import datetime as dt

from app.services.time_series import TimeSeriesService
from app.repos.stock_time_series_repo import StockTimeSeriesRepo

async def fetch_and_store_stock_time_series(symbol: str) -> int:
    """
    Function to fetch stock time series from provider and store them on our side.
    In case we already have the latest data in the database we don't perform 
    any unnecessary calls.

    Returns 1 in case a call to provider was made, 0 otherwise
    """
    # Check that we don't already have latest prices to avoid extra calls
    time_series_repo = StockTimeSeriesRepo()
    time_series = time_series_repo.get_symbol_time_series(symbol)

    if time_series:
        latest_timestamp = time_series[0].registered_date.date_ts
        latest_time_series_date = dt.datetime.fromtimestamp(latest_timestamp)
        current_date = dt.datetime.now()
        months_difference = (current_date.year - latest_time_series_date.year) * 12 + (current_date.month - latest_time_series_date.month)
        if months_difference < 1:
            return 0

    print("Fetching time series for:", symbol)
    await TimeSeriesService.scrape_and_store_stock_time_series(symbol)
    return 1
