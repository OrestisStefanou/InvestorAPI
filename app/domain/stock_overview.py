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
    eps: Optional[float] = None
    revenue_per_share: Optional[float] = None
    profit_margins: Optional[float] = None
    operating_margins: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    earnings_growth: Optional[float] = None
    revenue_growth: Optional[float] = None
    target_price: Optional[float] = None
    beta: Optional[float] = None
    price_to_sales_ratio: Optional[float] = None
    price_to_book_ratio: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
