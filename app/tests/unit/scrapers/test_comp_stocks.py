import pytest
from pytest_httpx import HTTPXMock

from app.services.ibd_scrapers.composite_stocks import CompositeStocksScraper


class TestTop200Scraper:
    @pytest.mark.asyncio
    async def test_get_top_200(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/top_200_comp_stocks.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/top-200-composite-stocks-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await CompositeStocksScraper.scrape_top_200_composite_stocks(day=19,month=10,year=2022)
        
        # Assert
        assert len(result) == 200

        # Assert first and last
        assert result[0].comp_rating.rating == 99
        assert result[0].eps_rating.rating == 99
        assert result[0].rs_rating.rating == 98
        assert result[0].acc_dis_rating.rating == "A-"
        assert result[0].fifty_two_wk_high.value == 17.2
        assert result[0].name == "CatalystPhr"
        assert result[0].symbol == "CPRX"
        assert result[0].closing_price.value == 15.23
        assert result[0].price_change_pct.value == -0.66
        assert result[0].vol_chg_pct.value == -45

        assert result[-1].comp_rating.rating == 93
        assert result[-1].eps_rating.rating == 89
        assert result[-1].rs_rating.rating == 90
        assert result[-1].acc_dis_rating.rating == "B-"
        assert result[-1].fifty_two_wk_high.value == 194.8
        assert result[-1].name == "ArthurJGallagr"
        assert result[-1].symbol == "AJG"
        assert result[-1].closing_price.value == 189.51
        assert result[-1].price_change_pct.value == 1.73
        assert result[-1].vol_chg_pct.value == -28

    @pytest.mark.asyncio
    async def test_get_bottom_200(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/bottom_200_comp_stocks.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/bottom-200-composite-stocks-oct-19-2022/',
            text=html_response
        )
        
        # Act
        result = await CompositeStocksScraper.scrape_bottom_200_composite_stocks(day=19,month=10,year=2022)
        
        # Assert
        assert len(result) == 200

        # Assert first and last
        assert result[0].comp_rating.rating == 1
        assert result[0].eps_rating.rating == 1
        assert result[0].rs_rating.rating == 1
        assert result[0].acc_dis_rating.rating == "E"
        assert result[0].fifty_two_wk_high.value == 304.3
        assert result[0].name == "Carvana A"
        assert result[0].symbol == "CVNA"
        assert result[0].closing_price.value == 8.55
        assert result[0].price_change_pct.value == -1.38
        assert result[0].vol_chg_pct.value == 7

        assert result[-1].comp_rating.rating == 16
        assert result[-1].eps_rating.rating == 5
        assert result[-1].rs_rating.rating == 21
        assert result[-1].acc_dis_rating.rating == "A-"
        assert result[-1].fifty_two_wk_high.value == 15.7
        assert result[-1].name == "TutorPerini"
        assert result[-1].symbol == "TPC"
        assert result[-1].closing_price.value == 7.08
        assert result[-1].price_change_pct.value == -0.14
        assert result[-1].vol_chg_pct.value == -49

    @pytest.mark.asyncio
    async def test_error_status_code(self, httpx_mock: HTTPXMock):
        # Prepare
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/top-200-composite-stocks-oct-19-2022/',
            status_code=404
        )
        
        # Act
        result = await CompositeStocksScraper.scrape_top_200_composite_stocks(day=19,month=10,year=2022)
        
        # Assert
        assert result is None
