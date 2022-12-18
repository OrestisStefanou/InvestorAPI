from dataclasses import dataclass

from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.comp_rating import CompRating
from app.domain.rs_rating import RsRating

@dataclass(frozen=True)
class StockLeader:
    name: str
    symbol: str
    closing_price: Price
    comp_rating: CompRating = None
    rs_rating: RsRating = None
    yield_pct: Percentage = None
    dividend_growth_pct: Percentage = None
    registered_date: str = None