import logging

from app import settings
from app.http.http_client import HttpClient
from app.domain.super_investor import SuperInvestor
from app.errors.http import HttpRequestError
from app.errors.dataroma import DataromaRequestError

class DataromaClient(HttpClient):
    def __init__(self) -> None:
        super().__init__(url=settings.dataroma_base_url)

        self._super_investor_map = {
            SuperInvestor.Warren_Buffet: 'BRK',
            SuperInvestor.Bill_Ackman: 'psc'
        }
    
    async def get_superinvestor_portfolio(self, super_investor: SuperInvestor) -> str:
        super_investor_symbol = self._super_investor_map[super_investor]
        try:
            response = await self.get(
                endpoint=f'/holdings.php?m={super_investor_symbol}'
            )
        except HttpRequestError as err:
            logging.error(f'Call to get {super_investor} portfolio failed with error: {str(err)}')
            raise DataromaRequestError(f"Failed to get {super_investor} portfolio")
        
        if response.status_code != 200:
            logging.error(f'Call to get {super_investor} portfolio failed with status: {response.status_code}')
            raise DataromaRequestError(f"Failed to get {super_investor} portfolio with status: {response.status_code}")

        return response.content

    async def get_superinvestor_grand_portfolio(self, page_num: int = 1) -> str:
        try:
            response = await self.get(
                endpoint=f'/g/portfolio.php?L={page_num}'
            )
        except HttpRequestError as err:
            logging.error(f'Call to get super_investor grand portfolio page {page_num} failed with error: {str(err)}')
            raise DataromaRequestError(f"Failed to get super_investor grand portfolio page {page_num}")
        
        if response.status_code != 200:
            logging.error(f'Call to get super_investor grand portfolio page {page_num} failed with status: {response.status_code}')
            raise DataromaRequestError(f"Failed to get super_investor grand portfolio page {page_num} with status: {response.status_code}")

        return response.content
