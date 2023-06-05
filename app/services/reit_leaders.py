from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper
from app.repos.reit_leaders_repo import ReitLeadersRepo
from app.domain.date import Date
from app.domain.stock_leader import StockLeader
from app.services.base_service import BaseService

class ReitLeadersService(BaseService):
    @classmethod
    async def scrape_and_store_reit_leaders_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        reit_leaders = await cls._scrape_reit_leaders_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if reit_leaders is None:
            logging.error(f"Error scraping reit_leaders for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape reit_leader')            

        # Store
        ReitLeadersRepo().add_stock_leaders_for_date(
            date=Date(day, month, year),
            data=reit_leaders
        )

    @classmethod
    async def _scrape_reit_leaders_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Scrape utility leaders from ibd website
        """
        reit_leaders = await StockLeadersScraper.scrape_reit_leaders(
            day, month, year
        )

        if reit_leaders is None:
            return None

        return reit_leaders

    def get_latest_reit_leaders(self) -> List[StockLeader]:
        return ReitLeadersRepo(self._db_session).get_latest_stock_leaders()
