from dataclasses import dataclass
from typing import Optional

from app.domain.sector import Sector

@dataclass(frozen=True)
class StockOverview:
    symbol: str
    sector: Sector
    market_cap: Optional[float] = None
    ebitda: Optional[float] = None
    forward_pe_ratio: Optional[float] = None
    trailing_pe_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    book_value: Optional[float] = None
    divided_per_share: Optional[float] = None
    dividend_yield: Optional[float] = None
    trailing_eps: Optional[float] = None
    forward_eps: Optional[float] = None
    revenue_per_share: Optional[float] = None
    profit_margins: Optional[float] = None
    operating_margins: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    earnings_growth: Optional[float] = None
    revenue_growth: Optional[float] = None
    target_high_price: Optional[float] = None
    target_low_price: Optional[float] = None
    target_mean_price: Optional[float] = None
    target_median_price: Optional[float] = None
