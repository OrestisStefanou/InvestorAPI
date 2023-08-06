from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CashFlow:
    symbol: str
    fiscal_date_ending: str
    reported_currency: str
    payments_for_operating_activities: Optional[float]
    operating_cashflow: Optional[float]
    proceeds_from_operating_activities: Optional[float]
    change_in_operating_liabilities: Optional[float]
    change_in_operating_assets: Optional[float]
    depreciation_depletion_and_amortization: Optional[float]
    capital_expenditures: Optional[float]
    change_in_receivables: Optional[float]
    change_in_inventory: Optional[float]
    profit_loss: Optional[float]
    cashflow_from_investment: Optional[float]
    cashflow_from_financing: Optional[float]
    proceeds_from_repayments_of_short_term_debt: Optional[float]
    payments_for_repurchase_of_common_stock: Optional[float]
    payments_for_repurchase_of_equity: Optional[float]
    payments_for_repurchase_of_preferred_stock: Optional[float]
    dividend_payout: Optional[float]
    dividend_payout_common_stock: Optional[float]
    dividend_payout_preferred_stock: Optional[float]
    proceeds_from_issuance_of_common_stock: Optional[float]
    proceeds_from_issuance_of_long_term_debt_and_capital_securities_net: Optional[float]
    proceeds_from_issuance_of_preferred_stock: Optional[float]
    proceeds_from_repurchase_of_equity: Optional[float]
    proceeds_from_sale_of_treasury_stock: Optional[float]
    change_in_cash_and_cash_equivalents: Optional[float]
    change_in_exchange_rate: Optional[float]
    net_income: Optional[float]
