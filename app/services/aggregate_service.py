from typing import List, Union

from app.domain.composite_stock import CompositeStock
from app.domain.stock_leader import StockLeader
from app.domain.symbol_appearances_count import SymbolAppearancesCount

class AggregateService:
    """
    Aggregate Base class
    """
    def get_appereances_count_for_each_symbol(self, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        raise NotImplementedError()
    
    def search_by_symbol(self, symbol: str) -> List[Union[CompositeStock, StockLeader]]:
        raise NotImplementedError()
