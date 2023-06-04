from enum import Enum
from typing import List

import pydantic

class EconomicIndicator(str, Enum):
    Treasury_Yield = 'Treasury_Yield'
    Interest_Rate = 'Interest_Rate'
    Inflation = 'Inflation'
    Unemployment = 'Unemployment'


class EconomicIndicatorTimeSeriesEntry(pydantic.BaseModel):
    value: float
    registered_date: str
    registered_date_ts: float


class EconomicIndicatorTimeSeries(pydantic.BaseModel):
    indicator: EconomicIndicator
    unit: str
    time_series: List[EconomicIndicatorTimeSeriesEntry]