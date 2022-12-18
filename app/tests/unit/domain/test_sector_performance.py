import pytest

from app.domain.sector_performance import SectorPriceChangePct

class TestSectorPriceChangePct:
    def test_ok(self) -> None:
        sector_price_pct = SectorPriceChangePct("+4.50%")
        assert sector_price_pct.change_pct == 4.50

        sector_price_pct = SectorPriceChangePct("-4.50%")
        assert sector_price_pct.change_pct == -4.50
    
    def test_value_error(self) -> None:
        with pytest.raises(ValueError):
            SectorPriceChangePct("+4.50")