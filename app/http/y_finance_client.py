import logging
import datetime as dt

from app import settings
from app.http.http_client import HttpClient
from app.errors.http import HttpRequestError
from app.domain.world_index import WorldIndex


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
        Returns html response of world index price series in 
        yahoo finance webiste
        """
        today = dt.datetime.today() # Get today's date and time
        five_years_ago = today - dt.timedelta(days=365*5) # Subtract 5 years' worth of days
        index_symbol = self._index_to_symbol_map.get(index)
        params = {
            'period1': int(five_years_ago.timestamp()),
            'period2': int(today.timestamp()),
            'interval': '1mo',
            'filter': 'history',
            'frequency': '1mo',
            'includeAdjustedClose': 'true'
        }
        try:
            response = await self.get(
                endpoint=f'/quote/{index_symbol}/history',
                params=params,
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error(f"Call to get world indices price series failed with error: {str(err)}")
            raise Exception()   # Create custom exception for this one

        if response.status_code != 200:
            return None

        return response.text
