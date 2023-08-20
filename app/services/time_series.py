from typing import List

from app import settings
from app.services.y_finance_scrapers.time_series import IndexTimeSeriesScraper
from app.services.alpha_vantage_scrapers.economic_indicators import EconomicIndicatorScraper
from app.services.alpha_vantage_scrapers.stock_time_series import StockTimeSeriesScraper
from app.domain.world_index import WorldIndex
from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry
from app.domain.time_series import StockTimeSeriesEntry
from app.domain.economic_indicator import EconomicIndicator
from app.repos.world_indices_time_series_repo import WorldIndicesTimeSeriesRepo
from app.repos.economic_indicators_repo import EconomicIndicatorTimeSeriesRepo
from app.repos.stock_time_series_repo import StockTimeSeriesRepo
from app.services.base_service import BaseService, timed_lru_cache


class TimeSeriesService(BaseService):
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
    async def _scrape_stock_time_series(
        cls,
        symbol: str,
    ) -> List[StockTimeSeriesEntry]:
        time_series = await StockTimeSeriesScraper.scrape_stock_time_series(symbol)
        return time_series

    @classmethod
    async def scrape_and_store_index_time_series(cls, index: WorldIndex):
        index_time_series = await cls._scrape_index_time_series(index)
        WorldIndicesTimeSeriesRepo().add_or_replace_time_series_for_index(
            index=index,
            time_series=index_time_series
        )

    @classmethod
    async def scrape_and_store_economic_indicator_time_series(cls, indicator: EconomicIndicator):
        indicator_time_series = await cls._scrape_economic_indicator_time_series(indicator)
        EconomicIndicatorTimeSeriesRepo().add_or_replace_time_series_for_indicator(
            indicator=indicator,
            time_series=indicator_time_series
        )

    @classmethod
    async def scrape_and_store_stock_time_series(cls, symbol: str):
        stock_time_series = await cls._scrape_stock_time_series(symbol)
        StockTimeSeriesRepo().add_or_replace_time_series_for_symbol(
            symbol=symbol,
            time_series=stock_time_series
        )

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_index_time_series(self, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        return WorldIndicesTimeSeriesRepo(self._db_session).get_index_time_series(
            index=index
        )

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_economic_indicator_time_series(self, indicator: EconomicIndicator) -> List[EconomicIndicatorTimeSeriesEntry]:
        return EconomicIndicatorTimeSeriesRepo(self._db_session).get_indicator_time_series(indicator)

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_stock_time_series(self, symbol: str) -> List[StockTimeSeriesEntry]:
        return StockTimeSeriesRepo(self._db_session).get_symbol_time_series(symbol)
