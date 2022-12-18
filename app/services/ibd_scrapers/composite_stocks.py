from typing import List, Optional

import pandas as pd

from app.http.ibd_client import IbdClient
from app.domain.composite_stock import CompositeStock
from app.domain.comp_rating import CompRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.acc_dis_rating import AccDisRating
from app.domain.price import Price
from app.domain.percentage import Percentage


class CompositeStocksScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> CompositeStock:
        return CompositeStock(
            comp_rating=CompRating(int(record[0])),
            eps_rating=EpsRating(int(record[1])),
            rs_rating=RsRating(int(record[2])),
            acc_dis_rating=AccDisRating(record[3]),
            fifty_two_wk_high=Price(record[4]),
            name=record[5],
            symbol=record[6],
            closing_price=Price(record[7]),
            price_change_pct=Percentage(record[8]),
            vol_chg_pct=Percentage(record[9])
        )

    @classmethod
    def scrape_composite_stocks(cls, html_response) -> Optional[List[CompositeStock]]:
        if html_response is None:
            return None

        tables = pd.read_html(html_response)
        composite_stocks_df = tables[0]

        composite_stocks_records = composite_stocks_df.to_records(index=False)
        # record example -> ('99', '99', '97', 'B+', '104.0', 'Denbury', 'DEN', '90.30', '-5.25', '58')
       
        # The first two rows containing column names and not the data
        # we are interested in so we skip them
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in composite_stocks_records[2:]
        ]


    @classmethod
    async def scrape_top_200_composite_stocks(cls, day: int, month: int, year: int) -> Optional[List[CompositeStock]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_top_200_composite_stocks(
            day, month, year
        )
        return cls.scrape_composite_stocks(html_response)

    @classmethod
    async def scrape_bottom_200_composite_stocks(cls, day: int, month: int, year: int) -> Optional[List[CompositeStock]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_bottom_200_composite_stocks(
            day, month, year
        )
        return cls.scrape_composite_stocks(html_response)
