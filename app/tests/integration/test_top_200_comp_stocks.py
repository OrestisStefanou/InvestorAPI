import asyncio
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.services.top_comp_stocks import TopCompositeStocksService
from app.domain.acc_dis_rating import AccDisRating
from app.domain.closing_price import ClosingPrice
from app.domain.comp_rating import CompRating
from app.domain.composite_stock import CompositeStock
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.main import app


class TestGetTop200CompStocks:
    def test_ok(self):
        # Prepare
        f = asyncio.Future()
        f.set_result(self._get_mock_composite_stocks())
        TopCompositeStocksService.get_top_200_comp_stocks_for_date = Mock(return_value=f)
        
        # Act
        client = TestClient(app)
        response = client.get("/top_200_composite_stocks?day=10&month=10&year=2022")

        # Assert
        assert response.status_code == 200
        assert response.json() == {
            'date': '10-10-2022', 
            'top_200_composite_stocks': [
                {
                    'comp_rating': 99,
                    'eps_rating': 99,
                    'rs_rating': 99,
                    'acc_dis_rating': 'A',
                    'fifty_two_wk_high': '500.00',
                    'name': 'Tesla',
                    'symbol': 'TSLA',
                    'closing_price': {'price': '450.00', 'change_pct': '13.00'},
                    'vol_chg_pct': '25.00'
                },
                {
                    'comp_rating': 99,
                    'eps_rating': 98,
                    'rs_rating': 96,
                    'acc_dis_rating': 'B',
                    'fifty_two_wk_high': '400.00',
                    'name': 'Amazon',
                    'symbol': 'AMZN',
                    'closing_price': {'price': '300.00', 'change_pct': '15.00'},
                    'vol_chg_pct': '23.00'
                }
            ]
        }

    def test_invalid_date(self):        
        # Act
        client = TestClient(app)
        response = client.get("/top_200_composite_stocks?day=35&month=10&year=2022")

        # Assert
        assert response.status_code == 400
        assert response.json() == {'detail': 'Invalid date'}

    def _get_mock_composite_stocks(self):
        return [
            CompositeStock(
                comp_rtg=CompRating(99),
                eps_rating=EpsRating(99),
                rs_rating=RsRating(99),
                acc_dis_rating=AccDisRating("A"),
                fifty_two_wk_high="500.00",
                name="Tesla",
                symbol="TSLA",
                closing_price=ClosingPrice(
                    price="450.00",
                    change_pct="13.00"
                ),
                vol_chg_pct="25.00"
            ),
            CompositeStock(
                comp_rtg=CompRating(99),
                eps_rating=EpsRating(98),
                rs_rating=RsRating(96),
                acc_dis_rating=AccDisRating("B"),
                fifty_two_wk_high="400.00",
                name="Amazon",
                symbol="AMZN",
                closing_price=ClosingPrice(
                    price="300.00",
                    change_pct="15.00"
                ),
                vol_chg_pct="23.00"
            ),
        ]