import time

from app.services.time_series import TimeSeriesService
from app.domain.economic_indicator import EconomicIndicator

async def scrape_and_store_economic_indicators_time_series():
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Interest_Rate)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Treasury_Yield)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Unemployment)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Global_Commodities_Index)
    # time.sleep(1)
    # await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Inflation)