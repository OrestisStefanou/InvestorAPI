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
            EconomicIndicator.Inflation: 'INFLATION',
            EconomicIndicator.Unemployment: 'UNEMPLOYMENT'
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

    async def get_company_overview(self, symbol: str) -> Dict[str, Any]:
        """
        Returns json response of company overview from alpha vantage.
        Example response: https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo
        """
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self._token
        }
        try:
            response = await self.get(
                endpoint='',
                params=params
            )
        except HttpRequestError as err:
            logging.error(f"Call to get {symbol} overview failed with error: {str(err)}")
            raise AlphaVantageRequestError(f"Call to get {symbol} overview failed with error: {str(err)}")
        
        if response.status_code != 200:
            logging.error(f"Call to get {symbol} overview failed with status: {response.status_code}")
            raise AlphaVantageRequestError(f"Call to get {symbol} overview failed, status: {response.status_code}, response {response.text}")

        return response.json()

    async def get_company_income_statements(self, symbol: str) -> Dict[str, Any]:
        """
        Returns json response of income statement from alpha vantage.
        Example response: https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo
        """
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': symbol,
            'apikey': self._token
        }
        try:
            response = await self.get(
                endpoint='',
                params=params
            )
        except HttpRequestError as err:
            logging.error(f"Call to get {symbol} income statement failed with error: {str(err)}")
            raise AlphaVantageRequestError(f"Call to get {symbol} income statement failed with error: {str(err)}")
        
        if response.status_code != 200:
            logging.error(f"Call to get {symbol} income statement failed with status: {response.status_code}")
            raise AlphaVantageRequestError(f"Call to get {symbol} income statement failed, status: {response.status_code}, response {response.text}")

        return response.json()

    async def get_company_balance_sheets(self, symbol: str) -> Dict[str, Any]:
        """
        Returns json response of balance sheet from alpha vantage.
        Example response: https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo
        """
        params = {
            'function': 'BALANCE_SHEET',
            'symbol': symbol,
            'apikey': self._token
        }
        try:
            response = await self.get(
                endpoint='',
                params=params
            )
        except HttpRequestError as err:
            logging.error(f"Call to get {symbol} balance sheets failed with error: {str(err)}")
            raise AlphaVantageRequestError(f"Call to get {symbol} balance sheets failed with error: {str(err)}")
        
        if response.status_code != 200:
            logging.error(f"Call to get {symbol} balance sheets failed with status: {response.status_code}")
            raise AlphaVantageRequestError(f"Call to get {symbol} balance sheets failed, status: {response.status_code}, response {response.text}")

        return response.json()

    async def get_company_cash_flows(self, symbol: str) -> Dict[str, Any]:
        """
        Returns json response of cash flow from alpha vantage.
        Example response: https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo
        """
        params = {
            'function': 'CASH_FLOW',
            'symbol': symbol,
            'apikey': self._token
        }
        try:
            response = await self.get(
                endpoint='',
                params=params
            )
        except HttpRequestError as err:
            logging.error(f"Call to get {symbol} cash flows failed with error: {str(err)}")
            raise AlphaVantageRequestError(f"Call to get {symbol} cash flows failed with error: {str(err)}")
        
        if response.status_code != 200:
            logging.error(f"Call to get {symbol} cash flows failed with status: {response.status_code}")
            raise AlphaVantageRequestError(f"Call to get {symbol} cash flows failed, status: {response.status_code}, response {response.text}")

        return response.json()
