from typing import List, Optional

import pandas as pd

from app.http.ibd_client import IbdClient
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.stock_leader import StockLeader


class StockLeadersScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> StockLeader:
        return StockLeader(
            name=str(record[0]),
            symbol=str(record[1]),
            closing_price=Price(str(record[2])),
            yield_pct=Percentage(str(record[3])),
            dividend_growth_pct=Percentage(str(record[4]))
        )

    @classmethod
    async def _scrape_stock_leaders(cls, html_response) -> Optional[List[StockLeader]]:
        tables = pd.read_html(html_response)
        stock_leaders_df = tables[0]

        stock_leaders_records = stock_leaders_df.to_records(index=False)
        # record example -> ('Mplx', 'MPLX', '33.52', '8.41', '11')
        # The first two rows containing column names and not the data
        # we are interested in so we skip them
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in stock_leaders_records[2:]
        ]

    @classmethod
    async def scrape_reit_leaders(cls, day: int, month: int, year: int) -> Optional[List[StockLeader]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_reit_leaders(
            day, month, year
        )

        if html_response is None:
            return None

        reit_leaders = await cls._scrape_stock_leaders(html_response)
        return reit_leaders

    @classmethod
    async def scrape_utility_leaders(cls, day: int, month: int, year: int) -> Optional[List[StockLeader]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_utility_leaders(
            day, month, year
        )

        if html_response is None:
            return None

        utility_leaders = await cls._scrape_stock_leaders(html_response)
        return utility_leaders

    @classmethod
    async def scrape_dividend_leaders(cls, day: int, month: int, year: int) -> Optional[List[StockLeader]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_dividend_leaders(
            day, month, year
        )

        if html_response is None:
            return None

        dividend_leaders = await cls._scrape_stock_leaders(html_response)
        return dividend_leaders
