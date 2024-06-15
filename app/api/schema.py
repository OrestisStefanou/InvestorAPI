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


class PredictionProbabilities(pydantic.BaseModel):
    up: float
    down: float


class PredictionFactors(pydantic.BaseModel):
    up: List[str]
    down: List[str]


class FundamentalsPricePrediction(pydantic.BaseModel):
    prediction_probabilites: PredictionProbabilities
    prediction_factors: PredictionFactors


class IncomeStatement(pydantic.BaseModel):
    fiscal_date_ending: str
    reported_currency: str
    gross_profit: float
    total_revenue:float
    cost_of_revenue:float
    cost_of_goods_and_services_sold:float
    operating_income:float
    selling_general_and_administrative:float
    research_and_development:float
    operating_expenses:float
    investment_income_net:float
    net_interest_income:float
    interest_income:float
    interest_expense:float
    non_interest_income:float
    other_non_operating_income:float
    depreciation:float
    depreciation_and_amortization:float
    income_before_tax:float
    income_tax_expense:float
    interest_and_debt_expense:float
    net_income_from_continuing_operations:float
    comprehensive_income_net_of_tax:float
    ebit:float
    ebitda:float
    net_income:float

    @pydantic.root_validator(pre=True)
    def check_none_values(cls, values):
        for key in values.keys():
            if key not in ['fiscal_date_ending', 'reported_currency']:
                if values[key] is None:
                    values[key] = 0.0

        return values


class BalanceSheet(pydantic.BaseModel):
    fiscal_date_ending: str
    reported_currency: str
    total_assets: float
    total_current_assets: float
    cash_and_cash_equivalents_at_carrying_value: float
    cash_and_short_term_investments: float
    inventory: float
    current_net_receivables: float
    total_non_current_assets: float
    property_plant_equipment: float
    accumulated_depreciation_amortization_ppe: float
    intangible_assets: float
    intangible_assets_excluding_goodwill: float
    goodwill: float
    investments: float
    long_term_investments: float
    short_term_investments: float
    other_current_assets: float
    other_non_current_assets: float
    total_liabilities: float
    total_current_liabilities: float
    current_accounts_payable: float
    deferred_revenue: float
    current_debt: float
    short_term_debt: float
    total_non_current_liabilities: float
    capital_lease_obligations: float
    long_term_debt: float
    current_long_term_debt: float
    long_term_debt_noncurrent: float
    short_long_term_debt_total: float
    other_current_liabilities: float
    other_non_current_liabilities: float
    total_shareholder_equity: float
    treasury_stock: float
    retained_earnings: float
    common_stock: float
    common_stock_shares_outstanding: float

    @pydantic.root_validator(pre=True)
    def check_none_values(cls, values):
        for key in values.keys():
            if key not in ['fiscal_date_ending', 'reported_currency']:
                if values[key] is None:
                    values[key] = 0.0

        return values


class CashFlow(pydantic.BaseModel):
    fiscal_date_ending: str
    reported_currency: str
    payments_for_operating_activities: float
    operating_cashflow: float
    proceeds_from_operating_activities: float
    change_in_operating_liabilities: float
    change_in_operating_assets: float
    depreciation_depletion_and_amortization: float
    capital_expenditures: float
    change_in_receivables: float
    change_in_inventory: float
    profit_loss: float
    cashflow_from_investment: float
    cashflow_from_financing: float
    proceeds_from_repayments_of_short_term_debt: float
    payments_for_repurchase_of_common_stock: float
    payments_for_repurchase_of_equity: float
    payments_for_repurchase_of_preferred_stock: float
    dividend_payout: float
    dividend_payout_common_stock: float
    dividend_payout_preferred_stock: float
    proceeds_from_issuance_of_common_stock: float
    proceeds_from_issuance_of_long_term_debt_and_capital_securities_net: float
    proceeds_from_issuance_of_preferred_stock: float
    proceeds_from_repurchase_of_equity: float
    proceeds_from_sale_of_treasury_stock: float
    change_in_cash_and_cash_equivalents: float
    change_in_exchange_rate: float
    net_income: float

    @pydantic.root_validator(pre=True)
    def check_none_values(cls, values):
        for key in values.keys():
            if key not in ['fiscal_date_ending', 'reported_currency']:
                if values[key] is None:
                    values[key] = 0.0

        return values


class StockFinancialsQuarterly(pydantic.BaseModel):
    balance_sheets: List[BalanceSheet]
    income_statements: List[IncomeStatement]
    cash_flows: List[CashFlow]


class ChatbotQuestion(pydantic.BaseModel):
    question: str
    session_id: str


class MessageSender(str, Enum):
    Agent = 'Agent'
    Human = 'Human'


class ConversationMessage(pydantic.BaseModel):
    message: str
    sender: MessageSender
