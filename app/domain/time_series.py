from dataclasses import dataclass

from app.domain.price import Price
from app.domain.date import Date

@dataclass(frozen=True)
class TimeSeriesEntry:
    registered_date: Date


@dataclass(frozen=True)
class IndexTimeSeriesEntry(TimeSeriesEntry):
    open_price: Price
    high_price: Price
    low_price: Price
    close_price: Price
    volume: float


@dataclass(frozen=True)
class EconomicIndicatorTimeSeriesEntry(TimeSeriesEntry):
    value: Price
    unit: str
