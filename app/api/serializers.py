from app.api import schema
from app.domain.time_series import EconomicIndicatorTimeSeriesEntry
from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.stock_leader import StockLeader


def serialize_economic_indicator_time_series_entry(
    time_series_entry: EconomicIndicatorTimeSeriesEntry
) -> schema.EconomicIndicatorTimeSeriesEntry:
    return schema.EconomicIndicatorTimeSeriesEntry(
        value=time_series_entry.value.value,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )


def serialize_index_time_series_entry(time_series_entry: IndexTimeSeriesEntry) -> schema.IndexTimeSeriesEntry:
    return schema.IndexTimeSeriesEntry(
        open_price=time_series_entry.open_price.value,
        high_price=time_series_entry.high_price.value,
        low_price=time_series_entry.low_price.value,
        close_price=time_series_entry.close_price.value,
        volume=time_series_entry.volume,
        registered_date=time_series_entry.registered_date.date_string,
        registered_date_ts=time_series_entry.registered_date.date_ts
    )


def serialize_dividend_leaders(dividend_leader: StockLeader) -> schema.DividendLeader:
    return schema.DividendLeader(
        symbol=dividend_leader.symbol,
        name=dividend_leader.name,
        yield_pct=dividend_leader.yield_pct.value,
        dividend_growth_pct=dividend_leader.dividend_growth_pct.value
    )
