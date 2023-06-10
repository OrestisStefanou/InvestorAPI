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


class Sector(str, Enum):
    ENERGY = "ENERGY"
    INSURNCE = "INSURNCE"
    COMPUTER = "COMPUTER"
    AGRICULTRE = "AGRICULTRE"
    AEROSPACE = "AEROSPACE"
    METALS = "METALS"
    FOOD_BEV = "FOOD_BEV"
    ELECTRNCS = "ELECTRNCS"
    APPAREL = "APPAREL"
    OFFICE = "OFFICE"
    MACHINE = "MACHINE"
    RETAIL = "RETAIL"
    ALCOHL_TOB = "ALCOHL_TOB"
    CHEMICAL = "CHEMICAL"
    BUSINS_SVC = "BUSINS SVC"
    MISC = "MISC"
    AUTO = "AUTO"
    UTILITY = "UTILITY"
    S_Ls = "S&Ls"
    BANKS = "BANKS"
    MEDICAL = "MEDICAL"
    CONSUMER = "CONSUMER"
    MINING = "MINING"
    TELECOM = "TELECOM"
    CHIPS = "CHIPS"
    MEDIA = "MEDIA"
    TRANSPRT = "TRANSPRT"
    BUILDING = "BUILDING"
    LEISURE = "LEISURE"
    REAL_EST = "REAL EST"
    SOFTWARE = "SOFTWARE"
    FINANCE = "FINANCE"
    INTERNET = "INTERNET"


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
	overall_rating: int
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


class SectorPerformance(pydantic.BaseModel):
    sector: Sector
    daily_price_change_pct: float
    start_of_year_price_change_pct: float


class SectorsPerformanceEntry(pydantic.BaseModel):
    date: str
    sectors_performance: List[SectorPerformance]


class SectorPerformanceEntry(pydantic.BaseModel):
    date: str
    sector_performance: SectorPerformance


class StockPerformance(pydantic.BaseModel):
	overall_rating: int
	eps_rating: int
	rs_rating: int
	closing_price: Optional[float] = None
	vol_chg_pct: Optional[float] = None
	acc_dis_rating: Optional[str] = None
	smr_rating: Optional[str] = None


class StockHistoricalPerformanceEntry(pydantic.BaseModel):
    date: str
    performance: StockPerformance


class StockHistoricalPerformance(pydantic.BaseModel):
    symbol: str
    name: str
    sector: Sector
    historical_performance: List[StockHistoricalPerformanceEntry]
