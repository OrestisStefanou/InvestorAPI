from typing import Optional, List

from app import settings
from app.domain.composite_stock import CompositeStock
from app.services.base_service import BaseService, timed_lru_cache
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo


class StocksService(BaseService):
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_stock_profile(self, symbol: str) -> Optional[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_stock_latest_data(symbol)
    
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_stock_historical_performance(
        self,
        symbol: str
    ) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_stock_historical_data(symbol)
    