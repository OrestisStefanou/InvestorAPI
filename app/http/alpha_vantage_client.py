import logging
from typing import Dict, Any

from app import settings
from app.http.http_client import HttpClient
from app.errors.http import HttpRequestError
from app.errors.alpha_vantage import AlphaVantageRequestError
from app.domain.economic_indicator import EconomicIndicator

class AlphaVantageClient(HttpClient):
    def __init__(self) -> None:
        super().__init__(url=settings.alpha_vantage_base_url)
        self._token = settings.alpha_vantage_token
    
    async def get_economic_indicator_time_series(self, indicator: EconomicIndicator) -> Dict[str, Any]:
        """
        Returns json response of global commodities
        index from alpha vantage.
        Example response: https://www.alphavantage.co/query?function=ALL_COMMODITIES&interval=monthly&apikey=demo
        """
        indicator_to_function_map = {
            EconomicIndicator.Global_Commodities_Index: 'ALL_COMMODITIES',
            EconomicIndicator.Treasury_Yield: 'TREASURY_YIELD',
            EconomicIndicator.Interest_Rate: 'FEDERAL_FUNDS_RATE',
            EconomicIndicator.Inflation: 'INFLATION'
        }

        params = {
            'function': indicator_to_function_map[indicator],
            'interval': 'monthly',
            'apikey': self._token
        }
        try:
            response = await self.get(
                endpoint='',
                params=params
            )
        except HttpRequestError as err:
            logging.error(f"Call to get {indicator.value} time series failed with error: {str(err)}")
            raise AlphaVantageRequestError(f"Call to get {indicator.value} time series failed with error: {str(err)}")
        
        if response.status_code != 200:
            logging.error(f"Call to get {indicator.value} time series failed with status: {response.status_code}")
            raise AlphaVantageRequestError(f"Call to get {indicator.value} time series failed, status: {response.status_code}, response {response.text}")

        return response.json()
