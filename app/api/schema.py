from enum import Enum
from typing import List, Optional

import pydantic

class EconomicIndicator(str, Enum):
    Treasury_Yield = 'Treasury_Yield'
    Interest_Rate = 'Interest_Rate'
    Inflation = 'Inflation'
    Unemployment = 'Unemployment'


class WorldIndex(str, Enum):
    S_P_500 = 'S&P 500'
    Dow_Jones_Ind_Avg = 'Dow Jones Industrial Average'
    Nasdaq_Composite = 'NASDAQ Composite'
    Nyse_Composite = 'NYSE COMPOSITE'


class EconomicIndicatorTimeSeriesEntry(pydantic.BaseModel):
    value: float
    registered_date: str
    registered_date_ts: float


class EconomicIndicatorTimeSeries(pydantic.BaseModel):
    indicator: EconomicIndicator
    unit: str
    time_series: List[EconomicIndicatorTimeSeriesEntry]


class IndexTimeSeriesEntry(pydantic.BaseModel):
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    registered_date: str
    registered_date_ts: float


class IndexTimeSeries(pydantic.BaseModel):
    index: WorldIndex
    time_series: List[IndexTimeSeriesEntry]


class CollectionStock(pydantic.BaseModel):
    symbol: str
    name: str


class StockLeader(CollectionStock):
    yield_pct: float
    dividend_growth_pct: float


class TechLeader(CollectionStock):
    comp_rating: int
    eps_rating: int
    rs_rating: int
    annual_eps_change_pct: Optional[float] = None
    last_qtr_eps_change_pct: Optional[float] = None
    next_qtr_eps_change_pct: Optional[float] = None
    last_qtr_sales_change_pct: Optional[float] = None
    return_on_equity: Optional[str] = None


class Stock(pydantic.BaseModel):
	comp_rating: int
	eps_rating: int
	rs_rating: int
	name: str
	symbol: str
	fifty_two_wk_high: Optional[float] = None
	closing_price: Optional[float] = None
	vol_chg_pct: Optional[float] = None
	acc_dis_rating: Optional[str] = None
	smr_rating: Optional[str] = None
	sector: Optional[str] = None
