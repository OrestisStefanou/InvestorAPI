from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper
from app.repos.dividend_leaders_repo import DividendLeadersRepo
from app.domain.date import Date
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.domain.stock_leader import StockLeader
from app.services.aggregate_service import AggregateService
from app.services.base_service import BaseService

class DividendLeadersService(BaseService, AggregateService):
    @classmethod
    async def scrape_and_store_dividend_leaders_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        dividend_leaders = await cls._scrape_dividend_leaders_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if dividend_leaders is None:
            logging.error(f"Error scraping dividend_leaders for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape dividend_leaders')            

        # Store
        DividendLeadersRepo().add_stock_leaders_for_date(
            date=Date(day, month, year),
            data=dividend_leaders
        )

    @classmethod
    async def _scrape_dividend_leaders_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Scrape dividend leaders from ibd website
        """
        dividend_leaders = await StockLeadersScraper.scrape_dividend_leaders(
            day, month, year
        )

        if dividend_leaders is None:
            return None

        return dividend_leaders

    def get_latest_dividend_leaders(self) -> List[StockLeader]:
        return DividendLeadersRepo(self._db_session).get_latest_stock_leaders()

    def get_appereances_count_for_each_symbol(self, limit: int = 100) -> List[SymbolAppearancesCount]:
        return DividendLeadersRepo(self._db_session).get_appereances_count_for_each_symbol(
            limit=limit
        )

    def search_by_symbol(self, symbol: str) -> List[StockLeader]:
        return DividendLeadersRepo(self._db_session).search_by_symbol(symbol)
