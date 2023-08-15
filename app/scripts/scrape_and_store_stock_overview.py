from datetime import datetime
import time
import asyncio

from app import dependencies
from app.repos.stock_overview_repo import StockOverviewRepo
from app.http.alpha_vantage_client import AlphaVantageClient
from app.domain.stock_overview import StockOverview
from app.domain.date import Date

DAY_LIMIT = 100
MINUTE_LIMIT = 5

def try_convert_to_float(value):
    if value is None:
        return None

    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return None


def fetch_and_store_stock_overview_for_symbol(symbol: str):
    now = datetime.now()

    stock_overview_repo = StockOverviewRepo()
    av_client = AlphaVantageClient()

    # Delete existing rows to avoid duplication
    stock_overview_repo.delete_stock_overview_for_symbol(symbol)

    company_info = asyncio.run(av_client.get_company_overview(symbol))

    stock_overview = StockOverview(
        symbol=symbol,
        sector=company_info.get('Sector') if company_info.get('Sector') else '',
        industry=company_info.get('Industry'),
        market_cap=try_convert_to_float(company_info.get('MarketCapitalization')),
        ebitda=try_convert_to_float(company_info.get('EBITDA')),
        pe_ratio=try_convert_to_float(company_info.get('PERatio')),
        forward_pe_ratio=try_convert_to_float(company_info.get('ForwardPE')),
        trailing_pe_ratio=try_convert_to_float(company_info.get('TrailingPE')),
        peg_ratio=try_convert_to_float(company_info.get('PEGRatio')),
        book_value=try_convert_to_float(company_info.get('BookValue')),
        divided_per_share=try_convert_to_float(company_info.get('DividendPerShare')),
        dividend_yield=try_convert_to_float(company_info.get('DividendYield')),
        eps=try_convert_to_float(company_info.get('EPS')),
        diluted_eps=try_convert_to_float(company_info.get('DilutedEPSTTM')),
        revenue_per_share=try_convert_to_float(company_info.get('RevenuePerShareTTM')),
        profit_margin=try_convert_to_float(company_info.get('ProfitMargin')),
        operating_margin=try_convert_to_float(company_info.get('OperatingMarginTTM')),
        return_on_assets=try_convert_to_float(company_info.get('ReturnOnAssetsTTM')),
        return_on_equity=try_convert_to_float(company_info.get('ReturnOnEquityTTM')),
        revenue=try_convert_to_float(company_info.get('RevenueTTM')),
        gross_profit=try_convert_to_float(company_info.get('GrossProfitTTM')),
        quarterly_earnings_growth_yoy=try_convert_to_float(company_info.get('QuarterlyEarningsGrowthYOY')),
        quarterly_revenue_growth_yoy=try_convert_to_float(company_info.get('QuarterlyRevenueGrowthYOY')),
        target_price=try_convert_to_float(company_info.get('AnalystTargetPrice')),
        beta=try_convert_to_float(company_info.get('Beta')),
        price_to_sales_ratio=try_convert_to_float(company_info.get('PriceToSalesRatioTTM')),
        price_to_book_ratio=try_convert_to_float(company_info.get('PriceToBookRatio')),
        ev_to_revenue=try_convert_to_float(company_info.get('EVToRevenue')),
        ev_to_ebitda=try_convert_to_float(company_info.get('EVToEBITDA')),
        outstanding_shares=try_convert_to_float(company_info.get('SharesOutstanding'))
    )

    stock_overview_repo.add_stock_overview_for_date(
        date=Date(day=now.day, month=now.month, year=now.year),
        stock_overview=stock_overview
    )
