from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper
from app.repos.reit_leaders_repo import ReitLeadersRepo
from app.domain.date import Date
from app.domain.stock_leader import StockLeader
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService


class ReitLeadersService(AggregateService):
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
        ReitLeadersRepo.add_stock_leaders_for_date(
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

    @classmethod
    def _fetch_reit_leaders_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        return ReitLeadersRepo.get_stock_leaders_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_reit_leaders_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Fetch reit leaders for given date from Redis
        """
        return ReitLeadersRepo.get_stock_leaders_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_reit_leaders_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        reit_leaders: List[StockLeader]
    ) -> None:
        ReitLeadersRepo.store_stock_leaders_for_date_in_cache(
            date=Date(day, month, year),
            data=reit_leaders
        )

    @classmethod
    async def get_reit_leaders_for_date(cls, day: int, month: int, year: int) -> List[StockLeader]:
        # Check if data exists in cache
        reit_leaders = cls._fetch_reit_leaders_for_date_from_cache(day, month, year)
        if reit_leaders:
            return reit_leaders

        # If not in cache check database
        reit_leaders = cls._fetch_reit_leaders_for_date_from_db(day, month, year)
        if reit_leaders:
            return reit_leaders

        # And if not in db as well scrape the data from ibd
        reit_leaders = await cls._scrape_reit_leaders_for_date(day, month, year)
        if reit_leaders:
            # Store in cache to avoid overloading ibd website
            cls._store_reit_leaders_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                reit_leaders=reit_leaders
            )
            return reit_leaders

        return []

    @classmethod
    def get_appereances_count_for_each_symbol(cls, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        return ReitLeadersRepo.get_appereances_count_for_each_symbol(
            min_count=min_count,
            limit=limit
        )

    @classmethod
    def search_by_symbol(cls, symbol: str) -> List[StockLeader]:
        return ReitLeadersRepo.search_by_symbol(symbol)
