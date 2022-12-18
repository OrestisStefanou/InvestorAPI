import logging

from app import settings
from app.http.http_client import HttpClient
from app.errors.http import HttpRequestError
from app.errors.ibd import IbdRequestError


class IbdClient(HttpClient):
    def __init__(self) -> None:
        super().__init__(url=settings.ibd_base_url)
        
        self._month_dict = {
            8: "aug",
            9: "sep",
            10: "oct",
            11: "nov",
            12: "dec"
        }

    def _get_month_name(self, month: int) -> str:
        return self._month_dict.get(month)

    def _get_day(self, day: int) -> str:
        if day < 10:
            return f'0{day}'
        
        return f'{day}'

    async def get_top_200_composite_stocks(self, day: int, month: int, year: int):
        """
        Returns html response of top 200 composite stocks in ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/top-200-composite-stocks-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get top 200 composite stocks failed with: ", str(err))
            raise IbdRequestError('Call to get top 200 composite stocks failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_bottom_200_composite_stocks(self, day: int, month: int, year: int):
        """
        Returns html response of bottom 200 composite stocks in ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/bottom-200-composite-stocks-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get bottom 200 composite stocks failed with: ", str(err))
            raise IbdRequestError('Call to get bottom 200 composite stocks failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_top_stocks_by_sector(self, day: int, month: int, year: int):
        """
        Returns html response of top stocks by sector ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/ibd-smart-nyse-nasdaq-tables-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get top stocks by sector failed with: ", str(err))
            raise IbdRequestError('Call to get top stocks by sector failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_stocks_up_in_price(self, day: int, month: int, year: int):
        """
        Returns html response of timesaver table from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/timesaver-table-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get timesaver tables failed with: ", str(err))
            raise IbdRequestError('Call to get timesaver tables failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_top_low_priced_stocks(self, day: int, month: int, year: int):
        """
        Returns html response of top ranked low priced stocks table from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/top-ranked-low-priced-stocks-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get top ranked low priced stocks table failed with: ", str(err))
            raise IbdRequestError('Call to get top ranked low priced stocks table failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_tech_leader_stocks(self, day: int, month: int, year: int):
        """
        Returns html response of tech leaders stocks table from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/ibd-tech-leaders-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get ibd tech leaders failed with: ", str(err))
            raise IbdRequestError('Call to get ibd tech leaders failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_dividend_leaders(self, day: int, month: int, year: int):
        """
        Returns html response of dividend leaders stocks table from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/dividend-leaders-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get dividend leaders failed with: ", str(err))
            raise IbdRequestError('Call to get dividend leaders failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_company_earnings_reports(self, day: int, month: int, year: int):
        """
        Returns html response of company earnings reports table from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/company-earnings-reports-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get company earnings reports failed with: ", str(err))
            raise IbdRequestError('Call to get company earnings reports failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_reit_leaders(self, day: int, month: int, year: int):
        """
        Returns html response of reit leaders response from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/reit-leaders-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get reit leaders failed with: ", str(err))
            raise IbdRequestError('Call to get reid leaders stocks failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_utility_leaders(self, day: int, month: int, year: int):
        """
        Returns html response of utility leaders response from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/utility-leaders-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get utility leaders failed with: ", str(err))
            raise IbdRequestError('Call to get utility leaders stocks failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_large_mid_cap_leaders_index(self, day: int, month: int, year: int):
        """
        Returns html response of large/mid cap leaders index response from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/ibd-large-mid-cap-leaders-index-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get large/mid cap leaders index failed with: ", str(err))
            raise IbdRequestError('Call to get large/mid cap leaders index failed')

        if response.status_code != 200:
            return None

        return response.text

    async def get_small_mid_cap_leaders_index(self, day: int, month: int, year: int):
        """
        Returns html response of small/mid cap leaders index response from ibd website
        """
        month_name = self._get_month_name(month)
        day_str = self._get_day(day)
        try:
            response = await self.get(
                endpoint=f"/ibd-small-mid-cap-leaders-index-{month_name}-{day_str}-{year}/",
                headers=self.headers
            )
        except HttpRequestError as err:
            logging.error("Call to get small/mid cap leaders index failed with: ", str(err))
            raise IbdRequestError('Call to get small/mid cap leaders index failed')

        if response.status_code != 200:
            return None

        return response.text
