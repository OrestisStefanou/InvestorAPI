from typing import Optional

from app.domain.composite_stock import CompositeStock
from app.services.base_service import BaseService
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo


class StocksService(BaseService):
    def get_stock_profile(self, symbol: str) -> Optional[CompositeStock]:
        return StocksWithSectorRepo(self._db_session).get_stock_latest_data(symbol)