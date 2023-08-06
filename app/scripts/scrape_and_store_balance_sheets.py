import asyncio

from app.repos.balance_sheet_repo import BalanceSheetRepo
from app.http.alpha_vantage_client import AlphaVantageClient
from app.domain.balance_sheet import BalanceSheet


def try_convert_to_float(value):
    if value is None:
        return None

    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return None


def fetch_and_store_balance_sheets_for_symbol(symbol: str):
    alpha_vantage_client = AlphaVantageClient()
    json_response = asyncio.run(alpha_vantage_client.get_company_balance_sheets(symbol))

    repo = BalanceSheetRepo()
    # Delete existing rows to avoid duplication
    repo.delete_balance_sheets_of_symbol(symbol)
    
    quarterly_reports = json_response['quarterlyReports']
    for report in quarterly_reports:
        balance_sheet = BalanceSheet(
            symbol=symbol,
            fiscal_date_ending=report['fiscalDateEnding'],
            reported_currency=report['reportedCurrency'],
            total_assets=try_convert_to_float(report['totalAssets']),
            total_current_assets=try_convert_to_float(report['totalCurrentAssets']),
            cash_and_cash_equivalents_at_carrying_value=try_convert_to_float(report['cashAndCashEquivalentsAtCarryingValue']),
            cash_and_short_term_investments=try_convert_to_float(report['cashAndShortTermInvestments']),
            inventory=try_convert_to_float(report['inventory']),
            current_net_receivables=try_convert_to_float(report['currentNetReceivables']),
            total_non_current_assets=try_convert_to_float(report['totalNonCurrentAssets']),
            property_plant_equipment=try_convert_to_float(report['propertyPlantEquipment']),
            accumulated_depreciation_amortization_ppe=try_convert_to_float(report['accumulatedDepreciationAmortizationPPE']),
            intangible_assets=try_convert_to_float(report['intangibleAssets']),
            intangible_assets_excluding_goodwill=try_convert_to_float(report['intangibleAssetsExcludingGoodwill']),
            goodwill=try_convert_to_float(report['goodwill']),
            investments=try_convert_to_float(report['investments']),
            long_term_investments=try_convert_to_float(report['longTermInvestments']),
            short_term_investments=try_convert_to_float(report['shortTermInvestments']),
            other_current_assets=try_convert_to_float(report['otherCurrentAssets']),
            other_non_current_assets=try_convert_to_float(report['otherNonCurrentAssets']),
            total_liabilities=try_convert_to_float(report['totalLiabilities']),
            total_current_liabilities=try_convert_to_float(report['totalCurrentLiabilities']),
            current_accounts_payable=try_convert_to_float(report['currentAccountsPayable']),
            deferred_revenue=try_convert_to_float(report['deferredRevenue']),
            current_debt=try_convert_to_float(report['currentDebt']),
            short_term_debt=try_convert_to_float(report['shortTermDebt']),
            total_non_current_liabilities=try_convert_to_float(report['totalNonCurrentLiabilities']),
            capital_lease_obligations=try_convert_to_float(report['capitalLeaseObligations']),
            long_term_debt=try_convert_to_float(report['longTermDebt']),
            current_long_term_debt=try_convert_to_float(report['currentLongTermDebt']),
            long_term_debt_noncurrent=try_convert_to_float(report['longTermDebtNoncurrent']),
            short_long_term_debt_total=try_convert_to_float(report['shortLongTermDebtTotal']),
            other_current_liabilities=try_convert_to_float(report['otherCurrentLiabilities']),
            other_non_current_liabilities=try_convert_to_float(report['otherNonCurrentLiabilities']),
            total_shareholder_equity=try_convert_to_float(report['totalShareholderEquity']),
            treasury_stock=try_convert_to_float(report['treasuryStock']),
            retained_earnings=try_convert_to_float(report['retainedEarnings']),
            common_stock=try_convert_to_float(report['commonStock']),
            common_stock_shares_outstanding=try_convert_to_float(report['commonStockSharesOutstanding']),
        )

        repo.add_balance_sheet(balance_sheet)
