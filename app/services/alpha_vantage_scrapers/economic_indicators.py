from typing import List
import datetime as dt

from app.http import alpha_vantage_client
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry
from app.domain.price import Price
from app.domain.date import Date
from app.domain.economic_indicator import EconomicIndicator
from app.errors.alpha_vantage import AlphaVantageParsingError

class EconomicIndicatorScraper:
    @classmethod
    def _convert_json_to_domain_model(cls, json) -> List[EconomicIndicatorTimeSeriesEntry]:
        unit = json['unit']
        time_series = []
        for entry in json['data']:
            # Convert datetime string to object
            date_time_obj = dt.datetime.strptime(entry['date'], '%Y-%m-%d')
            
            value=Price(entry['value'])
            if value.value is None:
                continue

            time_series.append(
                EconomicIndicatorTimeSeriesEntry(
                    registered_date=Date(
                        day=date_time_obj.day,
                        month=date_time_obj.month,
                        year=date_time_obj.year
                    ),
                    value=value,
                    unit=unit
                )
            )
        return time_series

    @classmethod
    async def scrape_economic_indicator_time_series(cls, indicator: EconomicIndicator):
        af_client = alpha_vantage_client.AlphaVantageClient()
        json_response = await af_client.get_economic_indicator_time_series(indicator)

        try:
            time_series = cls._convert_json_to_domain_model(json_response)
        except Exception as err:
            raise AlphaVantageParsingError(f'Failed to parse response for {indicator.value} time series with error: {str(err)}')
        
        return time_series
