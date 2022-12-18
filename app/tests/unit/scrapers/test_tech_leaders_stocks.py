import pytest
from pytest_httpx import HTTPXMock

from app.services.ibd_scrapers.tech_leaders_stocks import TechLeadersStocksScraper


class TestTechLeadersStocksScraper:
    @pytest.mark.asyncio
    async def test_ok(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/tech_leaders_stocks.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/ibd-tech-leaders-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await TechLeadersStocksScraper.scrape_tech_leaders_stocks(day=19,month=10,year=2022)

        # Assert
        assert result[0].comp_rating.rating == 99
        assert result[0].name == "Catalyst Pharma"
        assert result[0].symbol == "CPRX"
        assert result[0].price.value == 17.51
        assert result[0].eps_rating.rating == 99
        assert result[0].rs_rating.rating == 99
        assert result[0].annual_eps_change_pct.value == 33
        assert result[0].last_qtr_eps_change_pct.value == 86
        assert result[0].next_qtr_eps_change_pct.value == 54
        assert result[0].last_qtr_sales_change_pct.value == 59
        assert result[0].return_on_equity == "31"

        # Assert
        assert result[-1].comp_rating.rating == 64
        assert result[-1].name == "Dym Indstrs"
        assert result[-1].symbol == "DY"
        assert result[-1].price.value == 90.20
        assert result[-1].eps_rating.rating == 81
        assert result[-1].rs_rating.rating == 46
        assert result[-1].annual_eps_change_pct.value == 301
        assert result[-1].last_qtr_eps_change_pct.value == 89
        assert result[-1].next_qtr_eps_change_pct.value == None
        assert result[-1].last_qtr_sales_change_pct.value == 22
        assert result[-1].return_on_equity == "5"
