from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.composite_stocks import CompositeStocksScraper
from app.repos.top_composite_stocks_repo import TopCompositeStocksRepo
from app.domain.date import Date
from app.domain.composite_stock import CompositeStock
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService


class TopCompositeStocksService(AggregateService):
    @classmethod
    async def scrape_and_store_top_200_comp_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        top_200_comp_stocks = await cls._scrape_top_200_comp_stocks_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if top_200_comp_stocks is None:
            logging.error(f"Error scraping top 200 comp stocks for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape top 200 composite stocks')            

        # Store
        TopCompositeStocksRepo.add_comp_stocks_for_date(
            date=Date(day, month, year),
            data=top_200_comp_stocks
        )

    @classmethod
    async def _scrape_top_200_comp_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        """
        Scrape top 200 composite stocks from ibd website
        """
        top_200_comp_stocks = await CompositeStocksScraper.scrape_top_200_composite_stocks(
            day, month, year
        )

        if top_200_comp_stocks is None:
            return None

        if len(top_200_comp_stocks) != 200:
            logging.error(f"Error scraping top 200 comp stocks for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape top 200 composite stocks')

        return top_200_comp_stocks

    @classmethod
    def _fetch_top_200_comp_stocks_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        return TopCompositeStocksRepo.get_comp_stocks_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_top_200_comp_stocks_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        """
        Fetch top 200 composite stocks for given date from Redis
        """
        return TopCompositeStocksRepo.get_comp_stocks_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_top_200_comp_stocks_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        top_200_comp_stocks: List[CompositeStock]
    ) -> None:
        TopCompositeStocksRepo.store_comp_stocks_for_date_in_cache(
            date=Date(day, month, year),
            data=top_200_comp_stocks
        )

    @classmethod
    async def get_top_200_comp_stocks_for_date(cls, day: int, month: int, year: int) -> List[CompositeStock]:
        # Check if data exists in cache
        top_200_comp_stocks = cls._fetch_top_200_comp_stocks_for_date_from_cache(day, month, year)
        if top_200_comp_stocks:
            return top_200_comp_stocks

        # If not in cache check database
        top_200_comp_stocks = cls._fetch_top_200_comp_stocks_for_date_from_db(day, month, year)
        if top_200_comp_stocks:
            return top_200_comp_stocks

        # And if not in db as well scrape the data from ibd
        top_200_comp_stocks = await cls._scrape_top_200_comp_stocks_for_date(day, month, year)
        if top_200_comp_stocks:
            # Store in cache to avoid overloading ibd website
            cls._store_top_200_comp_stocks_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                top_200_comp_stocks=top_200_comp_stocks
            )
            return top_200_comp_stocks

        return []
    
    @classmethod
    def get_appereances_count_for_each_symbol(cls, min_count: int = 1, limit: int = 100) -> List[SymbolAppearancesCount]:
        """
        Returns how many times each symbol appeared in top composite stocks
        """
        return TopCompositeStocksRepo.get_appereances_count_for_each_symbol(min_count=min_count, limit=limit)
    
    @classmethod
    def search_by_symbol(cls, symbol: str) -> List[CompositeStock]:
        """
        Returns all occurences of given symbol in top composite stocks
        """
        return TopCompositeStocksRepo.search_by_symbol(symbol)
