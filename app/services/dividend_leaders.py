from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper
from app.repos.dividend_leaders_repo import DividendLeadersRepo
from app.domain.date import Date
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.domain.stock_leader import StockLeader
from app.services.aggregate_service import AggregateService


class DividendLeadersService(AggregateService):
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
        DividendLeadersRepo.add_stock_leaders_for_date(
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

    @classmethod
    def _fetch_dividend_leaders_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        return DividendLeadersRepo.get_stock_leaders_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_dividend_leaders_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[StockLeader]]:
        """
        Fetch dividend leaders for given date from Redis
        """
        return DividendLeadersRepo.get_stock_leaders_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_dividend_leaders_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        dividend_leaders: List[StockLeader]
    ) -> None:
        DividendLeadersRepo.store_stock_leaders_for_date_in_cache(
            date=Date(day, month, year),
            data=dividend_leaders
        )

    @classmethod
    def get_latest_dividend_leaders(cls) -> List[StockLeader]:
        return DividendLeadersRepo.get_latest_stock_leaders()

    @classmethod
    async def get_dividend_leaders_for_date(cls, day: int, month: int, year: int) -> List[StockLeader]:
        # Check if data exists in cache
        dividend_leaders = cls._fetch_dividend_leaders_for_date_from_cache(day, month, year)
        if dividend_leaders:
            return dividend_leaders

        # If not in cache check database
        dividend_leaders = cls._fetch_dividend_leaders_for_date_from_db(day, month, year)
        if dividend_leaders:
            return dividend_leaders

        # And if not in db as well scrape the data from ibd
        dividend_leaders = await cls._scrape_dividend_leaders_for_date(day, month, year)
        if dividend_leaders:
            # Store in cache to avoid overloading ibd website
            cls._store_dividend_leaders_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                dividend_leaders=dividend_leaders
            )
            return dividend_leaders

        return []

    @classmethod
    def get_appereances_count_for_each_symbol(cls, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        return DividendLeadersRepo.get_appereances_count_for_each_symbol(
            limit=limit
        )

    @classmethod
    def search_by_symbol(cls, symbol: str) -> List[StockLeader]:
        return DividendLeadersRepo.search_by_symbol(symbol)
