from typing import Optional, List, Dict, Any

from app import settings
from app.domain.composite_stock import CompositeStock
from app.services.base_service import BaseService, timed_lru_cache
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo
from app.repos.balance_sheet_repo import BalanceSheetRepo
from app.repos.income_statement_repo import IncomeStatementRepo
from app.repos.cash_flow_repo import CashFlowRepo

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
    
    @timed_lru_cache(minutes=settings.cache_time_minutes)
    def get_stock_financials(
        self,
        symbol: str
    ) -> Dict[str, Any]:
        """
        Returns a dictionary that contains the financials of a stock
        {
            'balance_sheets': List[BalanceSheet],
            'income_statements': List[IncomeStatement],
            'cash_flows': List[CashFlow]
        }
        """
        balance_sheets = BalanceSheetRepo(self._db_session).get_balance_sheets_for_symbol(symbol)
        income_statements = IncomeStatementRepo(self._db_session).get_income_statements_for_symbol(symbol)
        cash_flows = CashFlowRepo(self._db_session).get_cash_flows_for_symbol(symbol)
        return {
            'balance_sheets': balance_sheets,
            'income_statements': income_statements,
            'cash_flows': cash_flows
        }
