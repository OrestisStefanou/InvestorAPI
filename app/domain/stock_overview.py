from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StockOverview:
    symbol: str
    sector: str
    industry: str
    market_cap: Optional[float] = None
    ebitda: Optional[float] = None
    pe_ratio: Optional[float] = None
    forward_pe_ratio: Optional[float] = None
    trailing_pe_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    book_value: Optional[float] = None
    divided_per_share: Optional[float] = None
    dividend_yield: Optional[float] = None
    eps: Optional[float] = None
    diluted_eps: Optional[float] = None
    revenue_per_share: Optional[float] = None
    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    return_on_assets: Optional[float] = None
    return_on_equity: Optional[float] = None
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    quarterly_earnings_growth_yoy: Optional[float] = None
    quarterly_revenue_growth_yoy: Optional[float] = None
    target_price: Optional[float] = None
    beta: Optional[float] = None
    price_to_sales_ratio: Optional[float] = None
    price_to_book_ratio: Optional[float] = None
    ev_to_revenue: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    outstanding_shares: Optional[float] = None
