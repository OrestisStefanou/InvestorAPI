from typing import List

from app.domain.composite_stock import CompositeStock
from app.domain.sector import Sector
from app.domain.sector_performance import SectorPerformance
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo
from app.services.base_service import BaseService

class SectorService(BaseService):
    def get_sector_stocks(self, sector: Sector) -> List[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_sector_stocks(sector)
