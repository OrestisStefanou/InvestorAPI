from typing import List, Optional

import pandas as pd

from app.http.ibd_client import IbdClient
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.comp_rating import CompRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.percentage import Percentage
from app.domain.price import Price


class TechLeadersStocksScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> TechLeaderStock:
        return TechLeaderStock(
            comp_rating=CompRating(int(record[3])),
            eps_rating=EpsRating(int(record[4])),
            rs_rating=RsRating(int(record[5])),
            name=record[0],
            symbol=record[1],
            price=Price(record[2]),
            annual_eps_change_pct=Percentage(record[6]),
            last_qtr_eps_change_pct=Percentage(record[7]),
            next_qtr_eps_change_pct=Percentage(record[8]),
            last_qtr_sales_change_pct=Percentage(record[9]),
            return_on_equity=str(record[10])
        )

    @classmethod
    async def scrape_tech_leaders_stocks(cls, day: int, month: int, year: int) -> Optional[List[TechLeaderStock]]:
        ibd_client = IbdClient()
        html_response = await ibd_client.get_tech_leader_stocks(
            day, month, year
        )

        if html_response is None:
            return None

        tables = pd.read_html(html_response)
        tech_leaders_stocks_df = tables[0]

        tech_leaders_stocks_records = tech_leaders_stocks_df.to_records(index=False)
        # record example -> ('Clearfield', 'CLFD', '122.62', '99', '99', '99', '+113', '+109', '+51', '+84', '22', '18')
       
        # The first three rows containing column names and not the data
        # we are interested in so we skip them
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in tech_leaders_stocks_records[3:]
        ]
