import datetime as dt
from typing import List
import pandas as pd

from app.http import y_finance_client
from app.domain.world_index import WorldIndex
from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.price import Price
from app.domain.date import Date

class IndexTimeSeriesScraper:
    @classmethod
    def _convert_table_record_to_domain_model(cls, record) -> IndexTimeSeriesEntry:
        # Convert datetime string to object
        date_time_obj = dt.datetime.strptime(record[0], '%b %d, %Y')
        return IndexTimeSeriesEntry(
            registered_date=Date(
                day=date_time_obj.day,
                month=date_time_obj.month,
                year=date_time_obj.year
            ),
            open_price=Price(record[1]),
            high_price=Price(record[2]),
            low_price=Price(record[3]),
            close_price=Price(record[4]),
            volume=float(record[6])
        )
    
    @classmethod
    async def scrape_index_time_series(cls, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        yf_client = y_finance_client.YFinanceClient()
        html_response = await yf_client.get_world_index_time_series(index=index)
        if html_response is None:
            return None

        tables = pd.read_html(html_response)
        time_series_df = tables[0]
        time_series_records = time_series_df.to_records(index=False)
        # record example -> ('Apr 06, 2023', '4081.15', '4107.32', '4069.84', '4105.02', '4105.02', '2072470000')
        # The last record of the table contains useless data
        # so we ignore it
        return [
            cls._convert_table_record_to_domain_model(record)
            for record in time_series_records[:-1]
        ]
