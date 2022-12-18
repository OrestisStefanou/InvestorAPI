from typing import Any, Dict, List, Optional, Tuple
import json

from app.domain.acc_dis_rating import AccDisRating
from app.domain.comp_rating import CompRating
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.repos.sql_repo import SqlRepo
from app.repos.redis_repo import RedisRepo
from app.domain.composite_stock import CompositeStock
from app.domain.date import Date


class CompositeStockRepo(SqlRepo, RedisRepo):
	# Repos that inherit from this class must override table name
	_table_name = None

	@classmethod
	def _create_row_tuple_from_model(cls, composite_stock: CompositeStock, date: Date) -> Tuple[Any]:
		return (
			composite_stock.comp_rating.rating,
			composite_stock.eps_rating.rating,
			composite_stock.rs_rating.rating,
			composite_stock.acc_dis_rating.rating,
			composite_stock.fifty_two_wk_high.value,
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
			fifty_two_wk_high=Price(row[4]),
			name=row[5],
			symbol=row[6],
			closing_price=Price(row[7]),
			price_change_pct=Percentage(row[8]),
			vol_chg_pct=Percentage(row[9]),
			registered_date=row[10]
		)

	@classmethod
	def _serialize_composite_stock(cls, composite_stock: CompositeStock) -> Dict[str, Any]:
		return {
			"comp_rating": composite_stock.comp_rating.rating,
			"eps_rating": composite_stock.eps_rating.rating,
			"rs_rating": composite_stock.rs_rating.rating,
			"acc_dis_rating": composite_stock.acc_dis_rating.rating,
			"fifty_two_wk_high": composite_stock.fifty_two_wk_high.value,
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
			fifty_two_wk_high=Price(document.get('fifty_two_wk_high')),
			name=document.get('name'),
			symbol=document.get('symbol'),
			closing_price=Price(document.get('closing_price')),
			price_change_pct=Percentage(document.get('price_change_pct')),
			vol_chg_pct=Percentage(document.get('vol_chg_pct'))
		)

	@classmethod
	def _create_redis_key(cls, date: Date) -> str:
		return f'{cls._table_name}_{date.date_string}'

	@classmethod
	def add_comp_stocks_for_date(
		cls,
		date: Date,
		data: List[CompositeStock]
	) -> None:
		with cls._db_conn as con:
			con.executemany(
                f"INSERT INTO {cls._table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                [cls._create_row_tuple_from_model(composite_stock, date) for composite_stock in data]
            )

	@classmethod
	def get_comp_stocks_for_date(
		cls,
		date: Date,
		limit: int = 200
	) -> Optional[List[CompositeStock]]:
		cur = cls._db_conn.cursor()
		query =	f"""SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				price_change_pct,
				vol_chg_pct,
				registered_date 
			FROM {cls._table_name} 
			WHERE registered_date=? 
			LIMIT ?"""
		
		query_params = (date.date_string, limit)
		result = cur.execute(query, query_params)
		return [
			cls._create_model_from_row(row)
			for row in result
		]

	@classmethod
	def get_appereances_count_for_each_symbol(
		cls,
		min_count: Optional[int] = 1,
		limit: Optional[int] = 100
	) -> List[SymbolAppearancesCount]:
		cur = cls._db_conn.cursor()
		query = f"""SELECT 
					symbol,
					name,
					COUNT(*) 
				FROM {cls._table_name} 
				GROUP BY symbol
				HAVING COUNT(*) > ?
				ORDER BY COUNT(*) DESC
				LIMIT ?"""
		
		query_params = (min_count, limit)
		result = cur.execute(query, query_params)
		return [
			SymbolAppearancesCount(
				symbol=row[0],
				name=row[1],
				count=row[2]
			)
			for row in result
		]

	@classmethod
	def search_by_symbol(cls, symbol: str) -> Optional[List[CompositeStock]]:
		cur = cls._db_conn.cursor()
		query =	f"""SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				price_change_pct,
				vol_chg_pct,
				registered_date 
			FROM {cls._table_name} 
			WHERE symbol=?
			ORDER BY registered_date_ts DESC"""
		
		query_params = (symbol, )
		result = cur.execute(query, query_params)
		return [
			cls._create_model_from_row(row)
			for row in result
		]

	@classmethod
	def store_comp_stocks_for_date_in_cache(
		cls,
		date: Date,
		data: List[CompositeStock]
	) -> None:
		key = cls._create_redis_key(date)
		serialized_data = [cls._serialize_composite_stock(stock) for stock in data]
		cls._set_key_value(key, json.dumps(serialized_data))

	@classmethod
	def get_comp_stocks_for_date_from_cache(
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
