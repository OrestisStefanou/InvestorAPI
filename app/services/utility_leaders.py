from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper
from app.repos.utility_leaders_repo import UtilityLeadersRepo
from app.domain.date import Date
from app.domain.stock_leader import StockLeader
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.base_service import BaseService


class UtilityLeadersService(BaseService):
    @classmethod
    async def scrape_and_store_utility_leaders_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        utility_leaders = await cls._scrape_utility_leaders_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if utility_leaders is None:
            logging.error(f"Error scraping utility_leaders for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape utility_leader')            

        # Store
        UtilityLeadersRepo().add_stock_leaders_for_date(
            date=Date(day, month, year),
            data=utility_leaders
        )

    @classmethod
    async def _scrape_utility_leaders_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Scrape utility leaders from ibd website
        """
        utility_leaders = await StockLeadersScraper.scrape_utility_leaders(
            day, month, year
        )

        if utility_leaders is None:
            return None

        return utility_leaders

    def get_latest_utility_leaders(self) -> List[StockLeader]:
        return UtilityLeadersRepo(self._db_session).get_latest_stock_leaders()
