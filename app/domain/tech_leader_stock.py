from dataclasses import dataclass

from app.domain.comp_rating import CompRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.percentage import Percentage
from app.domain.price import Price

@dataclass(frozen=True)
class TechLeaderStock:
    name: str
    symbol: str
    price: Price
    comp_rating: CompRating
    eps_rating: EpsRating
    rs_rating: RsRating
    annual_eps_change_pct: Percentage
    last_qtr_eps_change_pct: Percentage
    next_qtr_eps_change_pct: Percentage
    last_qtr_sales_change_pct: Percentage
    return_on_equity: str
    registered_date: str = None
