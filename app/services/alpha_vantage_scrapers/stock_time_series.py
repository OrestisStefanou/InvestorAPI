import datetime as dt
from typing import List, Dict, Any

from app.http import alpha_vantage_client
from app.errors.alpha_vantage import AlphaVantageParsingError
from app.domain.time_series import StockTimeSeriesEntry
from app.domain.date import Date
from app.domain.price import Price

class StockTimeSeriesScraper:
    @classmethod
    def _convert_json_to_domain_model(cls, json: Dict[str, Any]) -> List[StockTimeSeriesEntry]:
        time_series = []

        for date, data in json['Weekly Adjusted Time Series'].items():
            # Convert datetime string to object
            date_time_obj = dt.datetime.strptime(date, '%Y-%m-%d')

            time_series.append(
                StockTimeSeriesEntry(
                    registered_date=Date(
                        day=date_time_obj.day,
                        month=date_time_obj.month,
                        year=date_time_obj.year
                    ),
                    open_price=Price(data["1. open"]),
                    high_price=Price(data["2. high"]),
                    low_price=Price(data["3. low"]),
                    close_price=Price(data["4. close"]),
                    volume=float(data["6. volume"]),
                    dividend_amount=float(data["7. dividend amount"])
                )
            )

        return time_series
    
    @classmethod
    async def scrape_stock_time_series(cls, symbol: str) -> List[StockTimeSeriesEntry]:
        av_client = alpha_vantage_client.AlphaVantageClient()
        json_response = await av_client.get_company_time_series(symbol)

        try:
            time_series = cls._convert_json_to_domain_model(json_response)
        except Exception as err:
            raise AlphaVantageParsingError(f'Failed to parse response for {symbol} time series with error: {str(err)}')
        
        return time_series
