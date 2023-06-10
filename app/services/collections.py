from typing import List

from app import settings
from app.domain.stock_leader import StockLeader
from app.domain.composite_stock import CompositeStock
from app.domain.tech_leader_stock import TechLeaderStock
from app.services.base_service import BaseService, timed_lru_cache
from app.repos.dividend_leaders_repo import DividendLeadersRepo
from app.repos.reit_leaders_repo import ReitLeadersRepo
from app.repos.utility_leaders_repo import UtilityLeadersRepo
from app.repos.tech_leaders_stocks_repo import TechLeadersStocksRepo
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo


class CollectionsService(BaseService):
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_dividend_leaders(self) -> List[StockLeader]:
        return DividendLeadersRepo(self._db_session).get_latest_stock_leaders()
    
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_reit_leaders(self) -> List[StockLeader]:
        return ReitLeadersRepo(self._db_session).get_latest_stock_leaders()
    
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_utility_leaders(self) -> List[StockLeader]:
        return UtilityLeadersRepo(self._db_session).get_latest_stock_leaders()

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_top_composite_stocks(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_top_overall_rated_stocks()
    
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_tech_leaders(self) -> List[TechLeaderStock]:
        return TechLeadersStocksRepo(self._db_session).get_latest_tech_leaders_stocks()
    
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_eps_rating_leaders(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_eps_rating_leaders()

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_price_rs_rating_leaders(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_rs_rating_leaders()

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_stocks_under_heavy_buying(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_stocks_under_heavy_buying()

    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_stocks_under_heavy_selling(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_stocks_under_heavy_selling()
