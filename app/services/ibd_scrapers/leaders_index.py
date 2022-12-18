from typing import List, Optional

import pandas as pd

from app.http.ibd_client import IbdClient
from app.domain.price import Price
from app.domain.stock_leader import StockLeader
from app.domain.comp_rating import CompRating
from app.domain.rs_rating import RsRating


class LeadersIndexScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> StockLeader:
        return StockLeader(
            comp_rating=CompRating(int(record[0])),
            rs_rating=RsRating(int(record[1])),
            name=record[2],
            symbol=record[3],
            closing_price=Price(record[4])
        )

    @classmethod
    async def _scrape_leaders_index(cls, html_response) -> Optional[List[StockLeader]]:
        tables = pd.read_html(html_response)
        leaders_index_df = tables[0]

        leaders_index_records = leaders_index_df.to_records(index=False)
        # record example -> ('99', '98', 'Futu', 'FUTU', '56.38')
        # The first row containing column names and not the data
        # we are interested in so we skip them
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in leaders_index_records[1:]
        ]

    @classmethod
    async def scrape_small_mid_cap_leaders_index(cls, day: int, month: int, year: int) -> Optional[List[StockLeader]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_small_mid_cap_leaders_index(
            day, month, year
        )

        if html_response is None:
            return None

        small_mid_cap_leaders_index = await cls._scrape_leaders_index(html_response)
        return small_mid_cap_leaders_index

    @classmethod
    async def scrape_large_mid_cap_leaders_index(cls, day: int, month: int, year: int) -> Optional[List[StockLeader]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_large_mid_cap_leaders_index(
            day, month, year
        )

        if html_response is None:
            return None

        large_mid_cap_leaders_index = await cls._scrape_leaders_index(html_response)
        return large_mid_cap_leaders_index
