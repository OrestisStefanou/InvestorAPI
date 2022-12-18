from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.tech_leaders_stocks import TechLeadersStocksScraper
from app.repos.tech_leaders_stocks_repo import TechLeadersStocksRepo
from app.domain.date import Date
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService


class TechLeadersStocksService(AggregateService):
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
        TechLeadersStocksRepo.add_tech_leaders_stocks_for_date(
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

    @classmethod
    def _fetch_tech_leaders_stocks_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[TechLeaderStock]]:
        return TechLeadersStocksRepo.get_tech_leaders_stocks_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_tech_leaders_stocks_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[TechLeaderStock]]:
        """
        Fetch tech leaders stocks for given date from Redis
        """
        return TechLeadersStocksRepo.get_tech_leaders_stocks_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_tech_leaders_stocks_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        tech_leaders_stocks: List[TechLeaderStock]
    ) -> None:
        TechLeadersStocksRepo.store_tech_leaders_stocks_for_date_in_cache(
            date=Date(day, month, year),
            data=tech_leaders_stocks
        )

    @classmethod
    async def get_tech_leaders_stocks_for_date(cls, day: int, month: int, year: int) -> List[TechLeaderStock]:
        # Check if data exists in cache
        tech_leaders_stocks = cls._fetch_tech_leaders_stocks_for_date_from_cache(day, month, year)
        if tech_leaders_stocks:
            return tech_leaders_stocks

        # If not in cache check database
        tech_leaders_stocks = cls._fetch_tech_leaders_stocks_for_date_from_db(day, month, year)
        if tech_leaders_stocks:
            return tech_leaders_stocks

        # And if not in db as well scrape the data from ibd
        tech_leaders_stocks = await cls._scrape_tech_leaders_stocks_for_date(day, month, year)
        if tech_leaders_stocks:
            # Store in cache to avoid overloading ibd website
            cls._store_tech_leaders_stocks_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                tech_leaders_stocks=tech_leaders_stocks
            )
            return tech_leaders_stocks

        return []

    @classmethod
    def get_appereances_count_for_each_symbol(cls, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        return TechLeadersStocksRepo.get_appereances_count_for_each_symbol(
            min_count=min_count,
            limit=limit
        )

    @classmethod
    def search_by_symbol(cls, symbol: str) -> List[TechLeaderStock]:
        return TechLeadersStocksRepo.search_by_symbol(symbol)
