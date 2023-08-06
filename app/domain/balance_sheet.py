from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class BalanceSheet:
    symbol: str
    fiscal_date_ending: str
    reported_currency: str
    total_assets: Optional[float]
    total_current_assets: Optional[float]
    cash_and_cash_equivalents_at_carrying_value: Optional[float]
    cash_and_short_term_investments: Optional[float]
    inventory: Optional[float]
    current_net_receivables: Optional[float]
    total_non_current_assets: Optional[float]
    property_plant_equipment: Optional[float]
    accumulated_depreciation_amortization_ppe: Optional[float]
    intangible_assets: Optional[float]
    intangible_assets_excluding_goodwill: Optional[float]
    goodwill: Optional[float]
    investments: Optional[float]
    long_term_investments: Optional[float]
    short_term_investments: Optional[float]
    other_current_assets: Optional[float]
    other_non_current_assets: Optional[float]
    total_liabilities: Optional[float]
    total_current_liabilities: Optional[float]
    current_accounts_payable: Optional[float]
    deferred_revenue: Optional[float]
    current_debt: Optional[float]
    short_term_debt: Optional[float]
    total_non_current_liabilities: Optional[float]
    capital_lease_obligations: Optional[float]
    long_term_debt: Optional[float]
    current_long_term_debt: Optional[float]
    long_term_debt_noncurrent: Optional[float]
    short_long_term_debt_total: Optional[float]
    other_current_liabilities: Optional[float]
    other_non_current_liabilities: Optional[float]
    total_shareholder_equity: Optional[float]
    treasury_stock: Optional[float]
    retained_earnings: Optional[float]
    common_stock: Optional[float]
    common_stock_shares_outstanding: Optional[float]
