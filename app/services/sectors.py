from collections import defaultdict
from typing import List, Dict

from app import settings
from app.domain.composite_stock import CompositeStock
from app.domain.sector import Sector
from app.domain.sector_performance import SectorPerformance
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo
from app.services.base_service import BaseService, timed_lru_cache


class SectorService(BaseService):
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_sector_stocks(self, sector: Sector) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_sector_stocks(sector)

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_sectors_performance(self) -> Dict[str, List[SectorPerformance]]:
        """
        Returns a dictionary with key the date in string format
        and value a list with the performance of each sector
        on that date
        """
        sectors_performance = StocksWithSectorRepo(self._db_session).get_sectors_performance()
        performance_dict = defaultdict(list)
        for performance_entry in sectors_performance:
            date = performance_entry.registered_date
            performance_dict[date].append(performance_entry)

        return performance_dict

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_sector_performance(self, sector: Sector) -> Dict[str, SectorPerformance]:
        """
        Returns a dictionary with key the date in string format
        and value the performance of the sector on that date
        """
        sectors_performance = StocksWithSectorRepo(self._db_session).get_sectors_performance(sector)
        performance_dict = defaultdict(list)
        for performance_entry in sectors_performance:
            date = performance_entry.registered_date
            performance_dict[date] = performance_entry

        return performance_dict