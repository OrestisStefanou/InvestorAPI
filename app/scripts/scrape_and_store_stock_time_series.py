from app.services.time_series import TimeSeriesService

async def fetch_and_store_stock_time_series(symbol: str):
    await TimeSeriesService.scrape_and_store_stock_time_series(symbol)
