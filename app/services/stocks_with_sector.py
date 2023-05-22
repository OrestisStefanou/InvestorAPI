import logging
from typing import List, Optional, Tuple

from app.domain.composite_stock import CompositeStock
from app.domain.date import Date
from app.domain.sector_performance import SectorPerformance
from app.domain.sector import Sector
from app.errors.ibd import IbdScrapeError
from app.services.ibd_scrapers.stocks_with_sector import StocksWithSectorScraper
from app.repos.stocks_with_sector_repo import StocksWithSectorRepo


class StocksWithSectorService:
    @classmethod
    async def scrape_and_store_stocks_with_sector_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ):
        # Scrape
        stocks_with_sector = await cls._scrape_stocks_with_sector_for_date(day, month, year)

        if stocks_with_sector is None:
            logging.error(f"Error scraping stocks with sector for date:{day}-{month}-{year}")
            raise IbdScrapeError('Failed to scrape stocks with sector')            

        StocksWithSectorRepo.add_stocks_with_sector_for_date(
            date=Date(day, month, year),
            sectors=stocks_with_sector[0],
            stocks=stocks_with_sector[1]
        )        

    @classmethod
    async def _scrape_stocks_with_sector_for_date(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[Tuple[List[SectorPerformance], List[List[CompositeStock]]]]:
        stocks_with_sector = await StocksWithSectorScraper.scrape_stocks_with_sector(
            day, month, year
        )
        return stocks_with_sector

    @classmethod
    def get_sector_stocks(
        cls,
        sector: Sector
    ) -> Optional[List[CompositeStock]]:
        return StocksWithSectorRepo.get_sector_stocks(sector)

    @classmethod
    def get_sectors_historical_performance(
        cls,
        sector: Optional[Sector] = None
    ) -> List[SectorPerformance]:
        return StocksWithSectorRepo.get_sectors_historical_performance(sector)

    @classmethod
    def get_stock_historical_data(
        cls,
        stock_symbol: str
    ) -> Optional[List[CompositeStock]]:
        return StocksWithSectorRepo.get_stock_historical_data(stock_symbol)

    @classmethod
    def get_eps_rating_leaders(cls) -> List[CompositeStock]:
        return StocksWithSectorRepo.get_eps_rating_leaders()

    @classmethod
    def get_rs_rating_leaders(cls) -> List[CompositeStock]:
        return StocksWithSectorRepo.get_rs_rating_leaders()
