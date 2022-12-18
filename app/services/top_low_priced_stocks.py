from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.top_low_priced_stocks import TopLowPricedStocksScraper
from app.repos.top_low_priced_stocks_repo import TopLowPricedStocksRepo
from app.domain.date import Date
from app.domain.composite_stock import CompositeStock


class TopLowPricedStocksService:
    @classmethod
    async def scrape_and_store_top_low_priced_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> None:
        # Scrape
        top_low_priced_stocks = await cls._scrape_top_low_priced_stocks_for_date(
            day, month, year
        )

        # This function should be called with arguments that will return data
        # so in case we got a None respose we raise an error
        if top_low_priced_stocks is None:
            logging.error(f"Error scraping top low priced stocks for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape top low priced stocks')            

        # Store
        TopLowPricedStocksRepo.add_top_low_priced_stocks_for_date(
            date=Date(day, month, year),
            data=top_low_priced_stocks
        )

    @classmethod
    async def _scrape_top_low_priced_stocks_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        """
        Scrape top low priced stocks from ibd website
        """
        top_low_priced_stocks = await TopLowPricedStocksScraper.scrape_top_low_priced_stocks(
            day, month, year
        )

        if top_low_priced_stocks is None:
            return None

        return top_low_priced_stocks

    @classmethod
    def _fetch_top_low_priced_stocks_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        return TopLowPricedStocksRepo.get_top_low_priced_stocks_for_date(
            date=Date(day, month, year)
        )

    @classmethod
    def _fetch_top_low_priced_stocks_for_date_from_cache(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[List[CompositeStock]]:
        """
        Fetch top low priced stocks for given date from Redis
        """
        return TopLowPricedStocksRepo.get_top_low_priced_stocks_for_date_from_cache(
            date=Date(day, month, year)
        )


    @classmethod
    def _store_top_low_priced_stocks_for_date_in_cache(
        cls,
        day: int,
        month: int,
        year: int,
        top_low_priced_stocks: List[CompositeStock]
    ) -> None:
        TopLowPricedStocksRepo.store_top_low_priced_stocks_for_date_in_cache(
            date=Date(day, month, year),
            data=top_low_priced_stocks
        )

    @classmethod
    async def get_top_low_priced_stocks_for_date(cls, day: int, month: int, year: int) -> List[CompositeStock]:
        # Check if data exists in cache
        top_low_priced_stocks = cls._fetch_top_low_priced_stocks_for_date_from_cache(day, month, year)
        if top_low_priced_stocks:
            return top_low_priced_stocks

        # If not in cache check database
        top_low_priced_stocks = cls._fetch_top_low_priced_stocks_for_date_from_db(day, month, year)
        if top_low_priced_stocks:
            return top_low_priced_stocks

        # And if not in db as well scrape the data from ibd
        top_low_priced_stocks = await cls._scrape_top_low_priced_stocks_for_date(day, month, year)
        if top_low_priced_stocks:
            # Store in cache to avoid overloading ibd website
            cls._store_top_low_priced_stocks_for_date_in_cache(
                day=day,
                month=month,
                year=year,
                top_low_priced_stocks=top_low_priced_stocks
            )
            return top_low_priced_stocks

        return []
