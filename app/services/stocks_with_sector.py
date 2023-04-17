import logging
from typing import List, Optional, Tuple

from app.domain.composite_stock import CompositeStock, StockWithSector
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
    def _fetch_stocks_with_sector_for_date_from_db(
        cls,
        day: int,
        month: int,
        year: int,
        sector: str = None
    ) -> Optional[List[StockWithSector]]:
        return StocksWithSectorRepo.get_stocks_with_sector_for_date(
            date=Date(day, month, year),
            sector=sector
        )

    @classmethod
    async def get_stocks_with_sector_for_date(
        cls,
        day: int,
        month: int,
        year: int,
        sector: str = None
    ) -> Optional[List[StockWithSector]]:
        # Check if data exists in cache
        stocks_with_sector = cls._fetch_stocks_with_sector_for_date_from_db(
            day, month, year, sector
        )
        return stocks_with_sector

    @classmethod
    def get_sectors_performance(
        cls,
        sector: Optional[Sector] = None
    ) -> List[SectorPerformance]:
        return StocksWithSectorRepo.get_sectors_performance(sector)
