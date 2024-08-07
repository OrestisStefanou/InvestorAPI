import logging
import datetime as dt

from app import settings
from app.http.http_client import HttpClient
from app.errors.http import HttpRequestError
from app.domain.world_index import WorldIndex
from app.errors.y_finance import YFinanceRequestError

class YFinanceClient(HttpClient):
    def __init__(self) -> None:
        super().__init__(url=settings.y_finance_base_url)

        self._index_to_symbol_map = {
            WorldIndex.S_P_500: '%5EGSPC',
            WorldIndex.Dow_Jones_Ind_Avg: '%5EDJI',
            WorldIndex.Nasdaq_Composite: '%5EIXIC',
            WorldIndex.Nyse_Composite: '%5ENYA'
        }

    async def get_world_index_time_series(self, index: WorldIndex):
        """
        Returns csv response of world index price series in 
        yahoo finance webiste
        """
        today = dt.datetime.today() # Get today's date and time
        five_years_ago = today - dt.timedelta(days=365*5) # Subtract 5 years' worth of days
        index_symbol = self._index_to_symbol_map.get(index)
        params = {
            'period1': int(five_years_ago.timestamp()),
            'period2': int(today.timestamp()),
            'interval': '1wk',
            'events': 'history',
            'includeAdjustedClose': 'true'
        }
        try:
            response = await self.get(
                endpoint=f'/finance/download/{index_symbol}',
                params=params,
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error(f"Call to get world indices price series failed with error: {str(err)}")
            raise YFinanceRequestError(f"Call to get world indices price series failed with error: {str(err)}")

        if response.status_code != 200:
            logging.error(f"Call to get world indices price series failed with status: {response.status_code}")
            raise YFinanceRequestError(f"Call to get world indices price series failed, status: {response.status_code}, response {response.text}")

        return response.content
