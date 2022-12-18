from typing import List, Optional

import pandas as pd

from app.domain.smr_rating import SmrRating
from app.http.ibd_client import IbdClient
from app.domain.composite_stock import CompositeStock
from app.domain.comp_rating import CompRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.acc_dis_rating import AccDisRating
from app.domain.closing_price import ClosingPrice


class StocksUpInPriceScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> CompositeStock:
        return CompositeStock(
            comp_rtg=CompRating(int(record[0])),
            eps_rating=EpsRating(int(record[1])),
            rs_rating=RsRating(int(record[2])),
            industry_group_strength=str(record[3]),
            smr_rating=SmrRating(str(record[4])),
            acc_dis_rating=AccDisRating(record[5]),
            fifty_two_wk_high=record[6],
            name=record[7],
            symbol=record[9],
            closing_price=ClosingPrice(
                price=record[10],
                change_pct=record[11]
            ),
            vol_chg_pct=record[12]
        )

    @classmethod
    async def scrape_top_stocks_up_in_price(cls, day: int, month: int, year: int) -> Optional[List[CompositeStock]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_stocks_up_in_price(
            day, month, year
        )

        if html_response is None:
            return None

        tables = pd.read_html(html_response)
        stocks_up_df = tables[0]

        stocks_up_records = stocks_up_df.to_records(index=False)
        # record example -> ('99', '99', '98', 'A+', 'A', 'B+', '324', 'EnphasEnrgy', nan, 'ENPH', '306.1', '+14.21', '+42')
        # Skip first record because it contains column names
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in stocks_up_records[1:]
        ]
