from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Earnings:
    symbol: str
    fiscal_date_ending: str
    reported_date: Optional[str]
    reported_eps: Optional[float]
    estimated_eps: Optional[float]
    surprise: Optional[float]
    surprise_percentage: Optional[float]
