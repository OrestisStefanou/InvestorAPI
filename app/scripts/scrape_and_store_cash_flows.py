import asyncio

from app.repos.cash_flow_repo import CashFlowRepo
from app.http.alpha_vantage_client import AlphaVantageClient
from app.domain.cash_flow import CashFlow


def try_convert_to_float(value):
    if value is None:
        return None

    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return None


def fetch_and_store_cash_flows_for_symbol(symbol: str):
    alpha_vantage_client = AlphaVantageClient()
    json_response = asyncio.run(alpha_vantage_client.get_company_cash_flows(symbol))

    repo = CashFlowRepo()
    # Delete existing rows to avoid duplication
    repo.delete_cash_flows_of_symbol(symbol)
    
    quarterly_reports = json_response['quarterlyReports']
    for report in quarterly_reports:
        cash_flow = CashFlow(
            symbol=symbol,
            fiscal_date_ending=report['fiscalDateEnding'],
            reported_currency=report['reportedCurrency'],
            payments_for_operating_activities=try_convert_to_float(report['paymentsForOperatingActivities']),
            operating_cashflow=try_convert_to_float(report['operatingCashflow']),
            proceeds_from_operating_activities=try_convert_to_float(report['proceedsFromOperatingActivities']),
            change_in_operating_liabilities=try_convert_to_float(report['changeInOperatingLiabilities']),
            change_in_operating_assets=try_convert_to_float(report['changeInOperatingAssets']),
            depreciation_depletion_and_amortization=try_convert_to_float(report['depreciationDepletionAndAmortization']),
            capital_expenditures=try_convert_to_float(report['capitalExpenditures']),
            change_in_receivables=try_convert_to_float(report['changeInReceivables']),
            change_in_inventory=try_convert_to_float(report['changeInInventory']),
            profit_loss=try_convert_to_float(report['profitLoss']),
            cashflow_from_investment=try_convert_to_float(report['cashflowFromInvestment']),
            cashflow_from_financing=try_convert_to_float(report['cashflowFromFinancing']),
            proceeds_from_repayments_of_short_term_debt=try_convert_to_float(report['proceedsFromRepaymentsOfShortTermDebt']),
            payments_for_repurchase_of_common_stock=try_convert_to_float(report['paymentsForRepurchaseOfCommonStock']),
            payments_for_repurchase_of_equity=try_convert_to_float(report['paymentsForRepurchaseOfEquity']),
            payments_for_repurchase_of_preferred_stock=try_convert_to_float(report['paymentsForRepurchaseOfPreferredStock']),
            dividend_payout=try_convert_to_float(report['dividendPayout']),
            dividend_payout_common_stock=try_convert_to_float(report['dividendPayoutCommonStock']),
            dividend_payout_preferred_stock=try_convert_to_float(report['dividendPayoutPreferredStock']),
            proceeds_from_issuance_of_common_stock=try_convert_to_float(report['proceedsFromIssuanceOfCommonStock']),
            proceeds_from_issuance_of_long_term_debt_and_capital_securities_net=try_convert_to_float(report['proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet']),
            proceeds_from_issuance_of_preferred_stock=try_convert_to_float(report['proceedsFromIssuanceOfPreferredStock']),
            proceeds_from_repurchase_of_equity=try_convert_to_float(report['proceedsFromRepurchaseOfEquity']),
            proceeds_from_sale_of_treasury_stock=try_convert_to_float(report['proceedsFromSaleOfTreasuryStock']),
            change_in_cash_and_cash_equivalents=try_convert_to_float(report['changeInCashAndCashEquivalents']),
            change_in_exchange_rate=try_convert_to_float(report['changeInExchangeRate']),
            net_income=try_convert_to_float(report['netIncome']),
        )

        repo.add_cash_flow(cash_flow)
