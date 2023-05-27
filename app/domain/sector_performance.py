from dataclasses import dataclass
from typing import Union, Optional

from app.domain.sector import Sector

class SectorPriceChangePct:
    def __init__(self, change_pct: Union[str, float], validate: bool = True) -> None:
        """
        If change_pct is a string validate must be true to do
        validation checks.
        If change_pct is a float validate must be false to skip
        validation checks that are expecting a string
        """
        if validate:
            if '%' not in change_pct:
                raise ValueError("SectorPriceChangePct does not contain %")
            
            try:
                float_change_pct = float(change_pct.replace('%', ''))
            except ValueError:
                float_change_pct = None
        else:
            float_change_pct = change_pct

        self._change_pct = float_change_pct

    @property
    def change_pct(self) -> float:
        return self._change_pct


@dataclass
class SectorPerformance:
    sector_name: Sector
    daily_price_change_pct: SectorPriceChangePct
    start_of_year_price_change_pct: SectorPriceChangePct
    registered_date: Optional[str] = None
    registered_date_ts: Optional[float] = None
