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
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Crude_Oil)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Natural_Gas)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Copper)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Aluminum)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Wheat)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Corn)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Cotton)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Sugar)
    time.sleep(1)
    await TimeSeriesService.scrape_and_store_economic_indicator_time_series(EconomicIndicator.Coffee)
