from typing import List, Optional, Tuple
import string

import bs4
import pandas as pd

from app.domain.acc_dis_rating import AccDisRating
from app.domain.comp_rating import CompRating
from app.domain.composite_stock import CompositeStock
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.sector_performance import SectorPriceChangePct, SectorPerformance
from app.domain.smr_rating import SmrRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.errors.ibd import IbdScrapeError
from app.http.ibd_client import IbdClient

class StocksWithSectorScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record):
        return CompositeStock(
            comp_rating=CompRating(int(record[0])),
            eps_rating=EpsRating(int(record[1])),
            rs_rating=RsRating(int(record[2])),
            smr_rating=SmrRating(record[3]),
            acc_dis_rating=AccDisRating(record[4]),
            fifty_two_wk_high=Price(str(record[5])),
            name=cls._scrape_stock_name_from_table_cell(record[6]),
            symbol=cls._scrape_stock_symbol_from_table_cell(record[7]),
            closing_price=Price(str(record[8])),
            price_change_pct=Percentage(str(record[9])),
            vol_chg_pct=Percentage(str(record[10]))
        )


    @classmethod
    def _scrape_sectors(cls, html_response) -> List[SectorPerformance]:
        soup = bs4.BeautifulSoup(html_response, "lxml")
        h3 = soup.find_all('h3')

        sector_data = []

        for header in h3:
            split_data = header.text.split(' ')
            if len(split_data) == 9 or len(split_data) == 10:
                if len(split_data) == 10:
                    sector_name = f'{split_data[1]} {split_data[2]}'
                    daily_change_pct = split_data[3]
                    change_since_Jan_1st = split_data[6]
                else:
                    sector_name = split_data[1]
                    daily_change_pct = split_data[2]
                    change_since_Jan_1st = split_data[5]
                sector_data.append(
                    SectorPerformance(
                        sector_name=sector_name,
                        daily_price_change_pct=SectorPriceChangePct(str(daily_change_pct)),
                        start_of_year_price_change_pct=SectorPriceChangePct(str(change_since_Jan_1st))
                    )
                )

        return sector_data

    @classmethod
    def _scrape_stock_name_from_table_cell(cls, stock_name_cell: str) -> str:
        # Replace html space with string space
        stock_name_cell = stock_name_cell.replace(u'\xa0', u' ')
        # Remove percentage if exists next to the name
        stock_name_cell = ' '.join([i for i in stock_name_cell.split() if not '.' in i])
        # Remove trailing spaces
        return stock_name_cell.strip()

    @classmethod
    def _scrape_stock_symbol_from_table_cell(cls, stock_symbol_cell: str) -> str:
        # Remove lowecase letters
        table = str.maketrans('', '', string.ascii_lowercase)
        stock_symbol_cell = stock_symbol_cell.translate(table)
        # Remove trailing spaces
        return stock_symbol_cell.strip()

    @classmethod
    def _scrape_stocks_tables(cls, html_response) -> List[List[CompositeStock]]:
        stocks_by_sector = []
        tables = pd.read_html(html_response)
        for table in tables:
            table_records = table.to_records(index=False)
            sector_stocks = []
            # Record example
            # ('83', '83', '90', 'C', 'B', '27.7', 'Enact\xa0Hldgs 2.3', 'ACT', '24.32', '+0.42', '-29', '164', '6', 'k')
            for record in table_records:
                try:
                    # To avoid scraping data that are not stocks
                    int(record[1])
                except Exception:
                    continue

                sector_stocks.append(cls._convert_table_record_to_domain_model(record))
            
            stocks_by_sector.append(sector_stocks)
        
        return stocks_by_sector

    @classmethod
    async def scrape_stocks_with_sector(
        cls,
        day: int,
        month: int,
        year: int
    ) -> Optional[Tuple[List[SectorPerformance], List[List[CompositeStock]]]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_top_stocks_by_sector(
            day, month, year
        )

        if html_response is None:
            return None

        sectors = cls._scrape_sectors(html_response)
        stocks = cls._scrape_stocks_tables(html_response)

        if len(sectors) != len(stocks):
            raise IbdScrapeError('Failed to scrape top stocks by sector')
        
        return sectors, stocks
