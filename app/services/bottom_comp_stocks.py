from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.composite_stocks import CompositeStocksScraper
from app.repos.bottom_composite_stocks_repo import BottomCompositeStocksRepo
from app.domain.date import Date
from app.domain.composite_stock import CompositeStock
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService


class BottomCompositeStocksService(AggregateService):
    @classmethod
    async def scrape_and_store_bottom_200_comp_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        top_200_comp_stocks = await cls._scrape_bottom_200_comp_stocks_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if top_200_comp_stocks is None:
            logging.error(f"Error scraping top 200 comp stocks for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape top 200 composite stocks')            

        # Store
        BottomCompositeStocksRepo.add_comp_stocks_for_date(
            date=Date(day, month, year),
            data=top_200_comp_stocks
        )

    @classmethod
    async def _scrape_bottom_200_comp_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        """
        Scrape bottom 200 composite stocks from ibd website
        """
        bottom_200_comp_stocks = await CompositeStocksScraper.scrape_bottom_200_composite_stocks(
            day, month, year
        )

        if bottom_200_comp_stocks is None:
            return None

        if len(bottom_200_comp_stocks) != 200:
            logging.error(f"Error scraping bottom 200 comp stocks for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape bottom 200 composite stocks')

        return bottom_200_comp_stocks

    @classmethod
    def _fetch_bottom_200_comp_stocks_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        return BottomCompositeStocksRepo.get_comp_stocks_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_bottom_200_comp_stocks_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        """
        Fetch bottom 200 composite stocks for given date from Redis
        """
        return BottomCompositeStocksRepo.get_comp_stocks_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_bottom_200_comp_stocks_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        bottom_200_comp_stocks: List[CompositeStock]
    ) -> None:
        BottomCompositeStocksRepo.store_comp_stocks_for_date_in_cache(
            date=Date(day, month, year),
            data=bottom_200_comp_stocks
        )

    @classmethod
    async def get_bottom_200_comp_stocks_for_date(cls, day: int, month: int, year: int) -> List[CompositeStock]:
        # Check if data exists in cache
        bottom_200_comp_stocks = cls._fetch_bottom_200_comp_stocks_for_date_from_cache(day, month, year)
        if bottom_200_comp_stocks:
            return bottom_200_comp_stocks

        # If not in cache check database
        bottom_200_comp_stocks = cls._fetch_bottom_200_comp_stocks_for_date_from_db(day, month, year)
        if bottom_200_comp_stocks:
            return bottom_200_comp_stocks

        # And if not in db as well scrape the data from ibd
        bottom_200_comp_stocks = await cls._scrape_bottom_200_comp_stocks_for_date(day, month, year)
        if bottom_200_comp_stocks:
            # Store in cache to avoid overloading ibd website
            cls._store_bottom_200_comp_stocks_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                bottom_200_comp_stocks=bottom_200_comp_stocks
            )
            return bottom_200_comp_stocks

        return []


    @classmethod
    def get_appereances_count_for_each_symbol(cls, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        """
        Returns how many times each symbol appeared in bottom composite stocks
        """
        return BottomCompositeStocksRepo.get_appereances_count_for_each_symbol(min_count=min_count, limit=limit)
    
    @classmethod
    def search_by_symbol(cls, symbol: str) -> List[CompositeStock]:
        """
        Returns all occurences of given symbol in bottom composite stocks
        """
        return BottomCompositeStocksRepo.search_by_symbol(symbol)
