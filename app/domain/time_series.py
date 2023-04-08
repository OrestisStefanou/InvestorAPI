from dataclasses import dataclass
from typing import List

from app.domain.price import Price

@dataclass(frozen=True)
class TimeSeriesEntry:
    registered_date: str


@dataclass(frozen=True)
class IndexTimeSeriesEntry(TimeSeriesEntry):
    open_price: Price
    high_price: Price
    low_price: Price
    close_price: Price
    volume: float
