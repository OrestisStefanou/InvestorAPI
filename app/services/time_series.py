from typing import List

from app.services.y_finance_scrapers.time_series import IndexTimeSeriesScraper
from app.domain.world_index import WorldIndex
from app.domain.time_series import IndexTimeSeriesEntry
from app.repos.world_indices_time_series_repo import WorldIndicesTimeSeriesRepo


class TimeSeriesService:
    @classmethod
    async def _scrape_index_time_series(cls, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        time_series = await IndexTimeSeriesScraper.scrape_index_time_series(index)
        return time_series

    @classmethod
    async def scrape_and_store_index_time_series(cls, index: WorldIndex):
        index_time_series = await cls._scrape_index_time_series(index)
        WorldIndicesTimeSeriesRepo.add_or_replace_time_series_for_index(
            index=index,
            time_series=index_time_series
        )

    @classmethod
    def get_index_time_series(cls, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        index_time_series = WorldIndicesTimeSeriesRepo.get_index_time_series(
            index=index
        )
        return index_time_series
