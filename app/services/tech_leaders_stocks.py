from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.tech_leaders_stocks import TechLeadersStocksScraper
from app.repos.tech_leaders_stocks_repo import TechLeadersStocksRepo
from app.domain.date import Date
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService
from app.services.base_service import BaseService


class TechLeadersStocksService(BaseService, AggregateService):
    @classmethod
    async def scrape_and_store_tech_leaders_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        tech_leaders_stocks = await cls._scrape_tech_leaders_stocks_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if tech_leaders_stocks is None:
            logging.error(f"Error scraping tech leaders stocks for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape tech leaders stocks')            

        # Store
        TechLeadersStocksRepo().add_tech_leaders_stocks_for_date(
            date=Date(day, month, year),
            data=tech_leaders_stocks
        )

    @classmethod
    async def _scrape_tech_leaders_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[TechLeaderStock]]:
        """
        Scrape tech leaders stocks from ibd website
        """
        tech_leaders_stocks = await TechLeadersStocksScraper.scrape_tech_leaders_stocks(
            day, month, year
        )

        if tech_leaders_stocks is None:
            return None

        return tech_leaders_stocks

    def get_latest_tech_leaders_stocks(self) -> List[TechLeaderStock]:
        return TechLeadersStocksRepo(self._db_session).get_latest_tech_leaders_stocks()

    def get_appereances_count_for_each_symbol(self, limit: int = 100) -> List[SymbolAppearancesCount]:
        return TechLeadersStocksRepo(self._db_session).get_appereances_count_for_each_symbol(
            limit=limit
        )

    def search_by_symbol(self, symbol: str) -> List[TechLeaderStock]:
        return TechLeadersStocksRepo(self._db_session).search_by_symbol(symbol)
