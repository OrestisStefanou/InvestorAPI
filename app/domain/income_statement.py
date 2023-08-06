from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class IncomeStatement:
    symbol: str
    fiscal_date_ending: str
    reported_currency: str
    gross_profit: Optional[float]
    total_revenue: Optional[float]
    cost_of_revenue: Optional[float]
    cost_of_goods_and_services_sold: Optional[float]
    operating_income: Optional[float]
    selling_general_and_administrative: Optional[float]
    research_and_development: Optional[float]
    operating_expenses: Optional[float]
    investment_income_net: Optional[float]
    net_interest_income: Optional[float]
    interest_income: Optional[float]
    interest_expense: Optional[float]
    non_interest_income: Optional[float]
    other_non_operating_income: Optional[float]
    depreciation: Optional[float]
    depreciation_and_amortization: Optional[float]
    income_before_tax: Optional[float]
    income_tax_expense: Optional[float]
    interest_and_debt_expense: Optional[float]
    net_income_from_continuing_operations: Optional[float]
    comprehensive_income_net_of_tax: Optional[float]
    ebit: Optional[float]
    ebitda: Optional[float]
    net_income: Optional[float]
