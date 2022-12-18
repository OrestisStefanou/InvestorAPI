from typing import Any, Dict, List, Optional, Tuple
import json

from app.domain.acc_dis_rating import AccDisRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.comp_rating import CompRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.repos.sql_repo import SqlRepo
from app.repos.redis_repo import RedisRepo
from app.domain.composite_stock import CompositeStock
from app.domain.date import Date


class TopLowPricedStocksRepo(SqlRepo, RedisRepo):
	"""
	Repo for top_low_priced_stocks table.
	"""
	@classmethod
	def _create_row_tuple_from_model(cls, composite_stock: CompositeStock, date: Date) -> Tuple[Any]:
		return (
			composite_stock.comp_rating.rating,
			composite_stock.eps_rating.rating,
			composite_stock.rs_rating.rating,
			composite_stock.acc_dis_rating.rating,
			composite_stock.year_high.value,
			composite_stock.name,
			composite_stock.symbol,
			composite_stock.closing_price.value,
			composite_stock.price_change_pct.value,
			composite_stock.vol_chg_pct.value,
			date.date_string,
			date.date_ts
		)

	@classmethod
	def _create_model_from_row(cls, row: Tuple[Any]) -> CompositeStock:
		return CompositeStock(
			comp_rating=CompRating(row[0]),
			eps_rating=EpsRating(row[1]),
			rs_rating=RsRating(row[2]),
			acc_dis_rating=AccDisRating(row[3]),
			year_high=Price(row[4]),
			name=row[5],
			symbol=row[6],
			closing_price=Price(row[7]),
			price_change_pct=Percentage(row[8]),
			vol_chg_pct=Percentage(row[9]),
			fifty_two_wk_high=None
		)

	@classmethod
	def _serialize_composite_stock(cls, composite_stock: CompositeStock) -> Dict[str, Any]:
		return {
			"comp_rating": composite_stock.comp_rating.rating,
			"eps_rating": composite_stock.eps_rating.rating,
			"rs_rating": composite_stock.rs_rating.rating,
			"acc_dis_rating": composite_stock.acc_dis_rating.rating,
			"year_high": composite_stock.year_high.value,
			"name": composite_stock.name,
			"symbol": composite_stock.symbol,
			"closing_price": composite_stock.closing_price.value,
			"price_change_pct": composite_stock.price_change_pct.value,
			"vol_chg_pct": composite_stock.vol_chg_pct.value
		}

	@classmethod
	def _deserialize_document(cls, document: Dict[str, Any]) -> CompositeStock:
		return CompositeStock(
			comp_rating=CompRating(document.get('comp_rating')),
			eps_rating=EpsRating(document.get('eps_rating')),
			rs_rating=RsRating(document.get('rs_rating')),
			acc_dis_rating=AccDisRating(document.get('acc_dis_rating')),
			year_high=Price(document.get('year_high')),
			name=document.get('name'),
			symbol=document.get('symbol'),
			closing_price=Price(document.get('closing_price')),
			price_change_pct=Percentage(document.get('price_change_pct')),
			vol_chg_pct=Percentage(document.get('vol_chg_pct')),
			fifty_two_wk_high=None
		)

	@classmethod
	def _create_redis_key(cls, date: Date):
		return f'top_low_priced_stocks_{date.date_string}'

	@classmethod
	def add_top_low_priced_stocks_for_date(
		cls,
		date: Date,
		data: List[CompositeStock]
	):
		with cls._db_conn as con:
			con.executemany(
                f"INSERT INTO top_low_priced_stocks VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                [cls._create_row_tuple_from_model(composite_stock, date) for composite_stock in data]
            )

	@classmethod
	def get_top_low_priced_stocks_for_date(
		cls,
		date: Date,
	) -> Optional[List[CompositeStock]]:
			cur = cls._db_conn.cursor()
			query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				year_high,
				name,
				symbol,
				closing_price,
				price_change_pct,
				vol_chg_pct 
			FROM top_low_priced_stocks 
			WHERE registered_date=?"""

			query_params =(date.date_string, )
			result = cur.execute(query, query_params)
			return [
				cls._create_model_from_row(row)
				for row in result
			]

	@classmethod
	def store_top_low_priced_stocks_for_date_in_cache(
		cls,
		date: Date,
		data: List[CompositeStock]
	) -> None:
		key = cls._create_redis_key(date)
		serialized_data = [cls._serialize_composite_stock(stock) for stock in data]
		cls._set_key_value(key, json.dumps(serialized_data))

	@classmethod
	def get_top_low_priced_stocks_for_date_from_cache(
		cls,
		date: Date
	) -> Optional[List[CompositeStock]]:
		key = cls._create_redis_key(date)
		json_data = cls._get_value_by_key(key)

		if json_data is None:
			return None

		return [
			cls._deserialize_document(stock)
			for stock in json.loads(json_data)
		]
