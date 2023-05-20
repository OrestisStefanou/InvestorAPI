import time

from app.domain.world_index import WorldIndex

from app.services.time_series import TimeSeriesService

async def scrape_and_store_world_indices_time_series():
    await TimeSeriesService.scrape_and_store_index_time_series(WorldIndex.S_P_500)
    time.sleep(10)
    await TimeSeriesService.scrape_and_store_index_time_series(WorldIndex.Dow_Jones_Ind_Avg)
    time.sleep(10)
    await TimeSeriesService.scrape_and_store_index_time_series(WorldIndex.Nasdaq_Composite)
    time.sleep(10)
    await TimeSeriesService.scrape_and_store_index_time_series(WorldIndex.Nyse_Composite)
    