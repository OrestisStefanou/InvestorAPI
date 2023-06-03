from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.leaders_index import LeadersIndexScraper
from app.repos.leaders_index_repo import LeadersIndexRepo
from app.repos.large_mid_cap_leaders_index_repo import LargeMidCapLeadersIndexRepo
from app.repos.small_mid_cap_leaders_index_repo import SmallMidCapLeadersIndexRepo
from app.domain.date import Date
from app.domain.stock_leader import StockLeader
from app.domain.symbol_appearances_count import SymbolAppearancesCount


class LeadersIndexService:

    _repo: LeadersIndexRepo = None
    _scrape_function = None

    @classmethod
    async def scrape_and_store_leaders_index_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        leaders_index = await cls._scrape_leaders_index_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if leaders_index is None:
            logging.error(f"Error scraping leaders index for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape leaders index')            

        # Store
        cls._repo.add_stock_leaders_for_date(
            date=Date(day, month, year),
            data=leaders_index
        )

    @classmethod
    async def _scrape_leaders_index_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Scrape leaders index from ibd website
        """
        leaders_index = await cls._scrape_function(
            day, month, year
        )

        if leaders_index is None:
            return None

        return leaders_index

    @classmethod
    def _fetch_leaders_index_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        return cls._repo.get_stock_leaders_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def get_latest_leaders_index(cls) -> List[StockLeader]:
        return  cls._repo.get_latest_stock_leaders()


class SmallMidCapLeadersIndexService(LeadersIndexService):
    _repo: LeadersIndexRepo = SmallMidCapLeadersIndexRepo()
    _scrape_function = LeadersIndexScraper.scrape_small_mid_cap_leaders_index


class LargeMidCapLeadersIndexService(LeadersIndexService):
    _repo: LeadersIndexRepo = LargeMidCapLeadersIndexRepo()
    _scrape_function = LeadersIndexScraper.scrape_large_mid_cap_leaders_index