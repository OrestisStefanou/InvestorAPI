from typing import List

from app.domain.stock_leader import StockLeader
from app.domain.composite_stock import CompositeStock
from app.domain.tech_leader_stock import TechLeaderStock
from app.services.base_service import BaseService
from app.repos.dividend_leaders_repo import DividendLeadersRepo
from app.repos.reit_leaders_repo import ReitLeadersRepo
from app.repos.utility_leaders_repo import UtilityLeadersRepo
from app.repos.tech_leaders_stocks_repo import TechLeadersStocksRepo
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo
from app.repos.top_composite_stocks_repo import TopCompositeStocksRepo


class CollectionsService(BaseService):
    def get_dividend_leaders(self) -> List[StockLeader]:
        return DividendLeadersRepo(self._db_session).get_latest_stock_leaders()
    
    def get_reit_leaders(self) -> List[StockLeader]:
        return ReitLeadersRepo(self._db_session).get_latest_stock_leaders()
    
    def get_utility_leaders(self) -> List[StockLeader]:
        return UtilityLeadersRepo(self._db_session).get_latest_stock_leaders()

    def get_top_composite_stocks(self) -> List[CompositeStock]:
        return TopCompositeStocksRepo(self._db_session).get_latest_comp_stocks()
    
    def get_tech_leaders(self) -> List[TechLeaderStock]:
        return TechLeadersStocksRepo(self._db_session).get_latest_tech_leaders_stocks()
    
    def get_eps_rating_leaders(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_eps_rating_leaders()

    def get_price_rs_rating_leaders(self) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_rs_rating_leaders()
