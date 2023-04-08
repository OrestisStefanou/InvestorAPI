import pandas as pd

from app.http import y_finance
from app.domain.world_index import WorldIndex

class TimeSeriesScraper:
    @classmethod
    def scrape_time_series(cls, html_response):
        if html_response is None:
            return None
        
        tables = pd.read_html(html_response)
        price_history_df = tables[0]

        print(price_history_df)
    
    @classmethod
    async def scrape_index_time_series(cls, index: WorldIndex):
        y_finance_client = y_finance.YFinanceClient()
        html_response = await y_finance_client.get_world_indices_time_series(index=index)
        return cls.scrape_time_series(html_response)
