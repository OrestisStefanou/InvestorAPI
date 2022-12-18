import pytest
from pytest_httpx import HTTPXMock

from app.services.ibd_scrapers.leaders_index import LeadersIndexScraper


class TestTopLowPricedStocksScraper:
    @pytest.mark.asyncio
    async def test_scrape_small_mid_cap_leaders_index(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/small_mid_cap_leaders_index.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/ibd-small-mid-cap-leaders-index-nov-23-2022/',
            text=html_response
        )
        
        # Act
        result = await LeadersIndexScraper.scrape_small_mid_cap_leaders_index(day=23,month=11,year=2022)

        # Assert first and last
        assert result[0].comp_rating.rating == 99
        assert result[0].rs_rating.rating == 99
        assert result[0].name == "Scorpio Tankers"
        assert result[0].symbol == "STNG"
        assert result[0].closing_price.value == 50.80

        assert result[-1].comp_rating.rating == 90
        assert result[-1].rs_rating.rating == 35
        assert result[-1].name == "Azz"
        assert result[-1].symbol == "AZZ"
        assert result[-1].closing_price.value == 41.10

    @pytest.mark.asyncio
    async def test_scrape_large_mid_cap_leaders_index(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/large_mid_cap_leaders_index.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/ibd-large-mid-cap-leaders-index-nov-23-2022/',
            text=html_response
        )
        
        # Act
        result = await LeadersIndexScraper.scrape_large_mid_cap_leaders_index(day=23,month=11,year=2022)

        # Assert first and last
        assert result[0].comp_rating.rating == 99
        assert result[0].rs_rating.rating == 98
        assert result[0].name == "Enphase Energy"
        assert result[0].symbol == "ENPH"
        assert result[0].closing_price.value == 315.78

        assert result[-1].comp_rating.rating == 90
        assert result[-1].rs_rating.rating == 66
        assert result[-1].name == "Pembina Pipeline"
        assert result[-1].symbol == "PBA"
        assert result[-1].closing_price.value == 35.34
