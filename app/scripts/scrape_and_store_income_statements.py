from datetime import datetime
import time
import asyncio

from app import dependencies
from app.repos.income_statement_repo import IncomeStatementRepo
from app.http.alpha_vantage_client import AlphaVantageClient
from app.domain.income_statement import IncomeStatement


def try_convert_to_float(value):
    if value is None:
        return None

    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return None


def fetch_and_store_income_statements_for_symbol(symbol: str):
    alpha_vantage_client = AlphaVantageClient()
    json_response = asyncio.run(alpha_vantage_client.get_company_income_statements(symbol))

    repo = IncomeStatementRepo()
    # Delete existing rows to avoid duplication
    repo.delete_income_statements_of_symbol(symbol)
    
    quarterly_reports = json_response['quarterlyReports']
    for report in quarterly_reports:
        income_statement = IncomeStatement(
            symbol=symbol,
            fiscal_date_ending=report['fiscalDateEnding'],
            reported_currency=report['reportedCurrency'],
            gross_profit=try_convert_to_float(report['grossProfit']),
            total_revenue=try_convert_to_float(report['totalRevenue']),
            cost_of_revenue=try_convert_to_float(report['costOfRevenue']),
            cost_of_goods_and_services_sold=try_convert_to_float(report['costofGoodsAndServicesSold']),
            operating_income=try_convert_to_float(report['operatingIncome']),
            selling_general_and_administrative=try_convert_to_float(report['sellingGeneralAndAdministrative']),
            research_and_development=try_convert_to_float(report['researchAndDevelopment']),
            operating_expenses=try_convert_to_float(report['operatingExpenses']),
            investment_income_net=try_convert_to_float(report['investmentIncomeNet']),
            net_interest_income=try_convert_to_float(report['netInterestIncome']),
            interest_income=try_convert_to_float(report['interestIncome']),
            interest_expense=try_convert_to_float(report['interestExpense']),
            non_interest_income=try_convert_to_float(report['nonInterestIncome']),
            other_non_operating_income=try_convert_to_float(report['otherNonOperatingIncome']),
            depreciation=try_convert_to_float(report['depreciation']),
            depreciation_and_amortization=try_convert_to_float(report['depreciationAndAmortization']),
            income_before_tax=try_convert_to_float(report['incomeBeforeTax']),
            income_tax_expense=try_convert_to_float(report['incomeTaxExpense']),
            interest_and_debt_expense=try_convert_to_float(report['interestAndDebtExpense']),
            net_income_from_continuing_operations=try_convert_to_float(report['netIncomeFromContinuingOperations']),
            comprehensive_income_net_of_tax=try_convert_to_float(report['comprehensiveIncomeNetOfTax']),
            ebit=try_convert_to_float(report['ebit']),
            ebitda=try_convert_to_float(report['ebitda']),
            net_income=try_convert_to_float(report['netIncome']),
        )

        repo.add_income_statement(income_statement)
