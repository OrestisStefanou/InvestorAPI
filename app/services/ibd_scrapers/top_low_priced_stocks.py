
from typing import List, Optional

import pandas as pd

from app.domain.acc_dis_rating import AccDisRating
from app.domain.comp_rating import CompRating
from app.domain.composite_stock import CompositeStock
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.http.ibd_client import IbdClient

class TopLowPricedStocksScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> CompositeStock:
        return CompositeStock(
            comp_rating=CompRating(int(record[0])),
            eps_rating=EpsRating(int(record[1])),
            rs_rating=RsRating(int(record[2])),
            acc_dis_rating=AccDisRating(record[3]),
            fifty_two_wk_high=None,   # We don't get this info here
            year_high=Price(record[4]),
            name=cls._scrape_stock_name_from_table_cell(record[5]),
            symbol=record[6],
            closing_price=Price(record[7]),
            price_change_pct=Percentage(record[8]),
            vol_chg_pct=Percentage(record[9])
        )

    @classmethod
    async def scrape_top_low_priced_stocks(cls, day: int, month: int, year: int) -> Optional[List[CompositeStock]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_top_low_priced_stocks(
            day, month, year
        )

        if html_response is None:
            return None

        tables = pd.read_html(html_response)
        low_priced_stocks_df = tables[0]

        low_priced_stocks_records = low_priced_stocks_df.to_records(index=False)
        # record example -> ('67', '78', '50', 'B+', '2.5', 'MereoBiophrma', 'MREO', '0.99', '0.00', '-19')

        # The first row containing column names and not the data
        # we are interested in so we skip them
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in low_priced_stocks_records[1:]
        ]

    @classmethod
    def _scrape_stock_name_from_table_cell(cls, stock_name_cell: str) -> str:
        # Replace html space with string space
        stock_name_cell = stock_name_cell.replace(u'\xa0', u' ')
        # Remove . character that exists if there was a percentage next to the name
        stock_name_cell = stock_name_cell.replace('.', '')
        # Remove trailing spaces
        return stock_name_cell.strip()
