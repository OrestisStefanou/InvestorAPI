import time
import asyncio

from app import dependencies
from app.repos.stock_overview_repo import StockOverviewRepo
from app.http.alpha_vantage_client import AlphaVantageClient
from app.domain.stock_overview import StockOverview
from app.domain.sector import Sector
from app.domain.date import Date

DAY_LIMIT = 500
MINUTE_LIMIT = 5

def try_convert_to_float(string_value):
    try:
        float_value = float(string_value)
        return float_value
    except ValueError:
        return None


with dependencies.get_db_conn() as conn:
    # Modify the query to fetch all the latest stock symbols that we have
    query = '''
        SELECT DISTINCT symbol, sector_name FROM stocks_with_sector WHERE sector_name = 'CHIPS'
    '''
    result = conn.execute(query)
    result = [('SMCI', 'CHIPS')]
    stock_overview_repo = StockOverviewRepo()
    av_client = AlphaVantageClient()

    for row in result:
        symbol = row[0]
        sector = Sector(row[1])
        
        company_info = asyncio.run(av_client.get_company_overview(symbol))
        stock_overview = StockOverview(
            symbol=symbol,
            sector=sector,
            market_cap=try_convert_to_float(company_info.get('MarketCapitalization')),
            ebitda=try_convert_to_float(company_info.get('EBITDA')),
            forward_pe_ratio=try_convert_to_float(company_info.get('ForwardPE')),
            trailing_pe_ratio=try_convert_to_float(company_info.get('TrailingPE')),
            peg_ratio=try_convert_to_float(company_info.get('PEGRatio')),
            book_value=try_convert_to_float(company_info.get('BookValue')),
            divided_per_share=try_convert_to_float(company_info.get('DividendPerShare')),
            dividend_yield=try_convert_to_float(company_info.get('DividendYield')),
            eps=try_convert_to_float(company_info.get('EPS')),
            revenue_per_share=try_convert_to_float(company_info.get('RevenuePerShareTTM')),
            profit_margins=try_convert_to_float(company_info.get('ProfitMargin')),
            operating_margins=try_convert_to_float(company_info.get('OperatingMarginTTM')),
            return_on_assets=try_convert_to_float(company_info.get('ReturnOnAssetsTTM')),
            return_on_equity=try_convert_to_float(company_info.get('ReturnOnEquityTTM')),
            revenue=try_convert_to_float(company_info.get('RevenueTTM')),
            gross_profit=try_convert_to_float(company_info.get('GrossProfitTTM')),
            earnings_growth=try_convert_to_float(company_info.get('QuarterlyEarningsGrowthYOY')),
            revenue_growth=try_convert_to_float(company_info.get('QuarterlyRevenueGrowthYOY')),
            target_price=try_convert_to_float(company_info.get('AnalystTargetPrice')),
            beta=try_convert_to_float(company_info.get('Beta')),
            price_to_sales_ratio=try_convert_to_float(company_info.get('PriceToSalesRatioTTM')),
            price_to_book_ratio=try_convert_to_float(company_info.get('PriceToBookRatio')),
            ev_to_revenue=try_convert_to_float(company_info.get('EVToRevenue')),
            ev_to_ebitda=try_convert_to_float(company_info.get('EVToEBITDA'))
        )

        stock_overview_repo.add_stock_overview_for_date(
            date=Date(day=25, month=6, year=2023),
            stock_overview=stock_overview
        )

        time.sleep(2)