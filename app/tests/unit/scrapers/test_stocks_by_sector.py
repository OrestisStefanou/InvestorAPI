import pytest
from pytest_httpx import HTTPXMock

from app.services.ibd_scrapers.stocks_with_sector import StocksWithSectorScraper

class TestStocksBySectorScraper:
    @pytest.mark.asyncio
    async def test_ok(self, httpx_mock: HTTPXMock):
        # Prepare
        with open('app/tests/ibd_responses/stocks_by_sector.html', mode='r') as f:
            html_response = f.read()
        
        httpx_mock.add_response(
            url='https://www.investors.com/data-tables/ibd-smart-nyse-nasdaq-tables-oct-19-2022/',
            text=html_response
        )
        
        # Act
        sectors, stocks = await StocksWithSectorScraper.scrape_stocks_with_sector(day=19,month=10,year=2022)

        # Assert first and last
        assert sectors[0].sector_name == "ENERGY"
        assert sectors[0].daily_price_change_pct.change_pct == 0.1
        assert sectors[0].start_of_year_price_change_pct.change_pct == 51.00
    
        assert stocks[0][0].comp_rating.rating == 97
        assert stocks[0][0].eps_rating.rating == 99
        assert stocks[0][0].rs_rating.rating == 97
        assert stocks[0][0].smr_rating.rating == "A"
        assert stocks[0][0].acc_dis_rating.rating == "B-"
        assert stocks[0][0].fifty_two_wk_high.value == 22.1
        assert stocks[0][0].name == "ComstckRes"
        assert stocks[0][0].symbol == "CRK"
        assert stocks[0][0].closing_price.value == 17.59
        assert stocks[0][0].price_change_pct.value == -0.35
        assert stocks[0][0].vol_chg_pct.value == -21

        assert stocks[0][-1].comp_rating.rating == 88
        assert stocks[0][-1].eps_rating.rating == 66
        assert stocks[0][-1].rs_rating.rating == 85
        assert stocks[0][-1].smr_rating.rating == "C"
        assert stocks[0][-1].acc_dis_rating.rating == "B+"
        assert stocks[0][-1].fifty_two_wk_high.value == 29.3
        assert stocks[0][-1].name == "WorldFuelSvc"
        assert stocks[0][-1].symbol == "INT"
        assert stocks[0][-1].closing_price.value == 28.05
        assert stocks[0][-1].price_change_pct.value == 0.17
        assert stocks[0][-1].vol_chg_pct.value == -29

        assert sectors[-1].sector_name == "FINANCE"
        assert sectors[-1].daily_price_change_pct.change_pct == 0.5
        assert sectors[-1].start_of_year_price_change_pct.change_pct == -33.93

        assert stocks[-1][0].comp_rating.rating == 91
        assert stocks[-1][0].eps_rating.rating == 95
        assert stocks[-1][0].rs_rating.rating == 86
        assert stocks[-1][0].smr_rating.rating == "B"
        assert stocks[-1][0].acc_dis_rating.rating == "B-"
        assert stocks[-1][0].fifty_two_wk_high.value == 28.0
        assert stocks[-1][0].name == "AsstmrkFinl"
        assert stocks[-1][0].symbol == "AMK"
        assert stocks[-1][0].closing_price.value == 23.67
        assert stocks[-1][0].price_change_pct.value == 0.21
        assert stocks[-1][0].vol_chg_pct.value == -24

        assert stocks[-1][-1].comp_rating.rating == 72
        assert stocks[-1][-1].eps_rating.rating == 94
        assert stocks[-1][-1].rs_rating.rating == 20
        assert stocks[-1][-1].smr_rating.rating == "A"
        assert stocks[-1][-1].acc_dis_rating.rating == "D-"
        assert stocks[-1][-1].fifty_two_wk_high.value == 36.4
        assert stocks[-1][-1].name == "XP Cl A"
        assert stocks[-1][-1].symbol == "XP"
        assert stocks[-1][-1].closing_price.value == 17.38
        assert stocks[-1][-1].price_change_pct.value == -0.23
        assert stocks[-1][-1].vol_chg_pct.value == -24
