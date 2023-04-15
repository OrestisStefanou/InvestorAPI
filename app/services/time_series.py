from typing import List

from app.services.y_finance_scrapers.time_series import IndexTimeSeriesScraper
from app.services.alpha_vantage_scrapers.economic_indicators import EconomicIndicatorScraper
from app.domain.world_index import WorldIndex
from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry
from app.domain.economic_indicator import EconomicIndicator
from app.repos.world_indices_time_series_repo import WorldIndicesTimeSeriesRepo
from app.repos.economic_indicators_repo import EconomicIndicatorTimeSeriesRepo


class TimeSeriesService:
    @classmethod
    async def _scrape_index_time_series(cls, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        time_series = await IndexTimeSeriesScraper.scrape_index_time_series(index)
        return time_series

    @classmethod
    async def _scrape_economic_indicator_time_series(
        cls,
        indicator: EconomicIndicator,
    ) -> List[EconomicIndicatorTimeSeriesEntry]:
        time_series = await EconomicIndicatorScraper.scrape_economic_indicator_time_series(indicator)
        return time_series

    @classmethod
    async def scrape_and_store_index_time_series(cls, index: WorldIndex):
        index_time_series = await cls._scrape_index_time_series(index)
        WorldIndicesTimeSeriesRepo.add_or_replace_time_series_for_index(
            index=index,
            time_series=index_time_series
        )

    @classmethod
    async def scrape_and_store_economic_indicator_time_series(cls, indicator: EconomicIndicator):
        indicator_time_series = await cls._scrape_economic_indicator_time_series(indicator)
        EconomicIndicatorTimeSeriesRepo.add_or_replace_time_series_for_indicator(
            indicator=indicator,
            time_series=indicator_time_series
        )

    @classmethod
    def get_index_time_series(cls, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        return WorldIndicesTimeSeriesRepo.get_index_time_series(
            index=index
        )

    @classmethod
    def get_economic_indicator_time_series(cls, indicator: EconomicIndicator) -> List[EconomicIndicatorTimeSeriesEntry]:
        return EconomicIndicatorTimeSeriesRepo.get_indicator_time_series(indicator)
