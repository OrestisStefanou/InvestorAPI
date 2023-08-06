import asyncio

from app.repos.earnings_repo import EarningsRepo
from app.http.alpha_vantage_client import AlphaVantageClient
from app.domain.earnings import Earnings


def try_convert_to_float(value):
    if value is None:
        return None

    try:
        float_value = float(value)
        return float_value
    except ValueError:
        return None


def fetch_and_store_earnings_for_symbol(symbol: str):
    alpha_vantage_client = AlphaVantageClient()
    json_response = asyncio.run(alpha_vantage_client.get_company_earnings(symbol))

    repo = EarningsRepo()
    # Delete existing rows to avoid duplication
    repo.delete_earnings_of_symbol(symbol)
    
    quarterly_earnings = json_response['quarterlyEarnings']
    for earnings in quarterly_earnings:
        e = Earnings(
            symbol=symbol,
            fiscal_date_ending=earnings['fiscalDateEnding'],
            reported_date=earnings['reportedDate'],
            reported_eps=try_convert_to_float(earnings['reportedEPS']),
            estimated_eps=try_convert_to_float(earnings['estimatedEPS']),
            surprise=try_convert_to_float(earnings['surprise']),
            surprise_percentage=try_convert_to_float(earnings['surprisePercentage'])
        )

        repo.add_earnings(earnings=e)
