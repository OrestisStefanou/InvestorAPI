from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper
from app.repos.utility_leaders_repo import UtilityLeadersRepo
from app.domain.date import Date
from app.domain.stock_leader import StockLeader
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService


class UtilityLeadersService(AggregateService):
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
        UtilityLeadersRepo.add_stock_leaders_for_date(
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

    @classmethod
    def _fetch_utility_leaders_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        return UtilityLeadersRepo.get_stock_leaders_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_utility_leaders_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Fetch utility leaders for given date from Redis
        """
        return UtilityLeadersRepo.get_stock_leaders_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_utility_leaders_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        utility_leaders: List[StockLeader]
    ) -> None:
        UtilityLeadersRepo.store_stock_leaders_for_date_in_cache(
            date=Date(day, month, year),
            data=utility_leaders
        )

    @classmethod
    async def get_utility_leaders_for_date(cls, day: int, month: int, year: int) -> List[StockLeader]:
        # Check if data exists in cache
        utility_leaders = cls._fetch_utility_leaders_for_date_from_cache(day, month, year)
        if utility_leaders:
            return utility_leaders

        # If not in cache check database
        utility_leaders = cls._fetch_utility_leaders_for_date_from_db(day, month, year)
        if utility_leaders:
            return utility_leaders

        # And if not in db as well scrape the data from ibd
        utility_leaders = await cls._scrape_utility_leaders_for_date(day, month, year)
        if utility_leaders:
            # Store in cache to avoid overloading ibd website
            cls._store_utility_leaders_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                utility_leaders=utility_leaders
            )
            return utility_leaders

        return []

    @classmethod
    def get_appereances_count_for_each_symbol(cls, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        return UtilityLeadersRepo.get_appereances_count_for_each_symbol(
            min_count=min_count,
            limit=limit
        )

    @classmethod
    def search_by_symbol(cls, symbol: str) -> List[StockLeader]:
        return UtilityLeadersRepo.search_by_symbol(symbol)
