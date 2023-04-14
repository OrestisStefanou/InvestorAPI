import logging

from app import settings
from app.http.http_client import HttpClient
from app.errors.http import HttpRequestError


class AlphaVantageClient(HttpClient):
    def __init__(self) -> None:
        super().__init__(url=settings.alpha_vantage_base_url)
        self._token = settings.alpha_vantage_token
    
    async def get_global_commodities_index(self):
        """
        Returns json response of global commodities
        index from alpha vantage.
        Example response: https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo
        """
        params = {
            'function': 'ALL_COMMODITIES',
            'interval': 'monthly',
            'apikey': self._token
        }
        try:
            response = await self.get(
                endpoint='',
                params=params
            )
        except HttpRequestError as err:
            logging.error(f"Call to get global commodities index failed with error: {str(err)}")
            raise Exception()