from typing import Optional, List
from enum import Enum

import strawberry as graphql


@graphql.type
class CompositeStock:
    comp_rating: int
    eps_rating: int
    rs_rating: int
    acc_dis_rating: str
    fifty_two_wk_high: Optional[float]
    name: str
    symbol: str
    closing_price: Optional[float]
    price_change_pct: Optional[float]
    vol_chg_pct: Optional[float]
    registered_date: Optional[str] = None


@graphql.type
class SectorStock(CompositeStock):
    smr_rating: str
    sector_name: str
    sector_daily_price_change_pct: str
    sector_start_of_year_price_change_pct: str   


@graphql.type
class SectorPerformance:
    sector_name: str
    daily_price_change_pct: float
    start_of_year_price_change_pct: float


@graphql.type
class LowPricedStock(CompositeStock):
    year_high: float
    fifty_two_wk_high: Optional[float] = None


@graphql.type
class TechLeaderStock:
    name: str
    symbol: str
    closing_price: float
    comp_rating: int
    eps_rating: int
    rs_rating: int
    annual_eps_change_pct: Optional[float] = None
    last_qtr_eps_change_pct: Optional[float] = None
    next_qtr_eps_change_pct: Optional[float] = None
    last_qtr_sales_change_pct: Optional[float] = None
    return_on_equity: Optional[str] = None
    registered_date: Optional[str] = None


@graphql.type
class StockLeader:
    name: str
    symbol: str
    closing_price: float
    yield_pct: float
    dividend_growth_pct: float
    registered_date: Optional[str] = None


@graphql.type
class LeadersIndexStock:
    comp_rating: int
    rs_rating: int
    stock_name: str
    stock_symbol: str
    closing_price: float
    registered_date: Optional[str] = None


@graphql.type
class StockAppereancesCount:
    symbol: str
    name: str
    count: int


@graphql.enum
class Collection(Enum):
    TopCompositeStocks = 'top_composite_stocks'
    BottomCompositeStocks = 'bottom_composite_stocks'
    DividendLeaders = 'dividend_leaders'
    UtilityLeaders = 'utility_leaders'
    ReitLeaders = 'reit_leaders'
    TechLeaders = 'tech_leaders'
    LargeMidCapLeadersIndex = 'large_mid_cap_leaders_index'
    SmallMidCapLeadersIndex = 'small_mid_cap_leaders_index'


@graphql.enum
class WorldIndex(Enum):
    S_P_500 = 'S&P 500'
    Dow_Jones_Ind_Avg = 'Dow Jones Industrial Average'
    Nasdaq_Composite = 'NASDAQ Composite'
    Nyse_Composite = 'NYSE COMPOSITE'


@graphql.type
class IndexTimeSeriesEntry:
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    registered_date: str
    registered_date_ts: float


@graphql.type
class IndexTimeSeries:
    index: WorldIndex
    time_series: List[IndexTimeSeriesEntry]