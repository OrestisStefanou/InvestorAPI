import pytest
from pytest_httpx import HTTPXMock

from app.services.ibd_scrapers.top_low_priced_stocks import TopLowPricedStocksScraper


class TestTopLowPricedStocksScraper:
    @pytest.mark.asyncio
    async def test_ok(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/top_low_price_stocks.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/top-ranked-low-priced-stocks-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await TopLowPricedStocksScraper.scrape_top_low_priced_stocks(day=19,month=10,year=2022)

        # Assert first and last
        assert result[0].comp_rating.rating == 77
        assert result[0].eps_rating.rating == 37
        assert result[0].rs_rating.rating == 98
        assert result[0].acc_dis_rating.rating == "A+"
        assert result[0].year_high.value == 16.0
        assert result[0].name == "89bio"
        assert result[0].symbol == "ETNB"
        assert result[0].closing_price.value == 8.19
        assert result[0].price_change_pct.value == -0.00
        assert result[0].vol_chg_pct.value == -54

        assert result[-1].comp_rating.rating == 71
        assert result[-1].eps_rating.rating == 47
        assert result[-1].rs_rating.rating == 83
        assert result[-1].acc_dis_rating.rating == "A"
        assert result[-1].year_high.value == 21.4
        assert result[-1].name == "Zymeworks"
        assert result[-1].symbol == "ZYME"
        assert result[-1].closing_price.value == 8.04
        assert result[-1].price_change_pct.value == 0.28
        assert result[-1].vol_chg_pct.value == -50
