from dataclasses import dataclass
from typing import Optional

from app.domain.comp_rating import CompRating
from app.domain.acc_dis_rating import AccDisRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.smr_rating import SmrRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.sector import Sector

@dataclass(frozen=True)
class CompositeStock:
	comp_rating: CompRating
	eps_rating: EpsRating
	rs_rating: RsRating
	name: str
	symbol: str
	fifty_two_wk_high: Price = None
	closing_price: Price = None
	price_change_pct: Percentage = None
	vol_chg_pct: Percentage = None
	acc_dis_rating: AccDisRating = None
	smr_rating: Optional[SmrRating] = None
	sector: Optional[Sector] = None
	industry_group_strength: Optional[str] = None
	year_high: Optional[Price] = None
	registered_date: Optional[str] = None


@dataclass(frozen=True)
class StockWithSector(CompositeStock):
	sector_name: str = None
	sector_daily_price_change_pct: Percentage = None
	sector_start_of_year_price_change_pct: Percentage = None
