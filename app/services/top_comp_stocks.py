from typing import List, Optional
import logging

from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.composite_stocks import CompositeStocksScraper
from app.repos.top_composite_stocks_repo import TopCompositeStocksRepo
from app.domain.date import Date
from app.domain.composite_stock import CompositeStock
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.services.aggregate_service import AggregateService
from app.services.base_service import BaseService

class TopCompositeStocksService(BaseService, AggregateService):
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
        TopCompositeStocksRepo().add_comp_stocks_for_date(
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

    def get_latest_top_comp_stocks(self, limit: int = 100) -> List[CompositeStock]:
        return TopCompositeStocksRepo(self._db_session).get_latest_comp_stocks(limit=limit)
    
    def get_appereances_count_for_each_symbol(self, limit: int = 100) -> List[SymbolAppearancesCount]:
        """
        Returns how many times each symbol appeared in top composite stocks
        """
        return TopCompositeStocksRepo(self._db_session).get_appereances_count_for_each_symbol(limit=limit)
    
    def search_by_symbol(self, symbol: str) -> List[CompositeStock]:
        """
        Returns all occurences of given symbol in top composite stocks
        """
        return TopCompositeStocksRepo(self._db_session).search_by_symbol(symbol)
