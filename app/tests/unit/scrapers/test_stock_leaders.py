import pytest
from pytest_httpx import HTTPXMock

from app.services.ibd_scrapers.stock_leaders import StockLeadersScraper


class TestStockLeadersScraper:
    @pytest.mark.asyncio
    async def test_scrape_reit_leaders_ok(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/reit_leaders.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/reit-leaders-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await StockLeadersScraper.scrape_reit_leaders(day=19,month=10,year=2022)

        # Assert
        assert result[0].name == "Ready Capital"
        assert result[0].symbol == "RC"
        assert result[0].closing_price.value == 12.90
        assert result[0].yield_pct.value == 13.02
        assert result[0].dividend_growth_pct.value == 12

        assert result[-1].name == "Lxp Industrial Trust"
        assert result[-1].symbol == "LXP"
        assert result[-1].closing_price.value == 10.78
        assert result[-1].yield_pct.value == 4.45
        assert result[-1].dividend_growth_pct.value == 6

    @pytest.mark.asyncio
    async def test_scrape_utility_leaders_ok(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/utility_leaders.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/utility-leaders-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await StockLeadersScraper.scrape_utility_leaders(day=19,month=10,year=2022)

        # Assert
        assert result[0].name == "Oge Energy"
        assert result[0].symbol == "OGE"
        assert result[0].closing_price.value == 38.56
        assert result[0].yield_pct.value == 4.25
        assert result[0].dividend_growth_pct.value == 3

        assert result[-1].name == "Wec Energy Group"
        assert result[-1].symbol == "WEC"
        assert result[-1].closing_price.value == 94.15
        assert result[-1].yield_pct.value == 3.09
        assert result[-1].dividend_growth_pct.value == 7

    @pytest.mark.asyncio
    async def test_scrape_dividend_leaders_ok(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/dividend_leaders.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/dividend-leaders-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await StockLeadersScraper.scrape_dividend_leaders(day=19,month=10,year=2022)

        # Assert
        assert result[0].name == "Mplx"
        assert result[0].symbol == "MPLX"
        assert result[0].closing_price.value == 33.93
        assert result[0].yield_pct.value == 9.14
        assert result[0].dividend_growth_pct.value == 8

        assert result[-1].name == "T Rowe Price Group"
        assert result[-1].symbol == "TROW"
        assert result[-1].closing_price.value == 133.34
        assert result[-1].yield_pct.value == 3.60
        assert result[-1].dividend_growth_pct.value == 25
