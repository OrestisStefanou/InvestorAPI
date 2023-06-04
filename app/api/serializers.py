from app.api import schema
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry


def serialize_economic_indicator_time_series_entry(
    time_series_entry: EconomicIndicatorTimeSeriesEntry
) -> schema.EconomicIndicatorTimeSeriesEntry:
    return schema.EconomicIndicatorTimeSeriesEntry(
        value=time_series_entry.value.value,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )
