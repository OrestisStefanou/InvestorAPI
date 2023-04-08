from app.services.y_finance_scrapers.time_series import TimeSeriesScraper
from app.domain.world_index import WorldIndex

class TimeSeriesService:
    @classmethod
    async def scrape_index_time_series(cls, index: WorldIndex):
        await TimeSeriesScraper.scrape_index_time_series(index)


import asyncio

asyncio.run(TimeSeriesService.scrape_index_time_series(index=WorldIndex.S_P_500))