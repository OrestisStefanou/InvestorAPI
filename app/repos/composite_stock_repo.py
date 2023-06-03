from typing import Any, List, Optional, Tuple

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
			vol_chg_pct=Percentage(row[8]),
			registered_date=row[9]
		)

	def add_comp_stocks_for_date(
		self,
		date: Date,
		data: List[CompositeStock]
	) -> None:
		with self._db_conn as con:
			con.executemany(
                f"INSERT INTO {self._table_name} VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                [self._create_row_tuple_from_model(composite_stock, date) for composite_stock in data]
            )

	def get_comp_stocks_for_date(
		self,
		date: Date,
		limit: int = 200
	) -> Optional[List[CompositeStock]]:
		cur = self._db_conn.cursor()
		query =	f"""SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
				registered_date 
			FROM {self._table_name} 
			WHERE registered_date=? 
			LIMIT ?"""
		
		query_params = (date.date_string, limit)
		result = cur.execute(query, query_params)
		return [
			self._create_model_from_row(row)
			for row in result
		]

	def get_latest_comp_stocks(
		self,
		limit: int = 200
	) -> Optional[List[CompositeStock]]:
		cur = self._db_conn.cursor()
		query =	f"""SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
				registered_date 
			FROM {self._table_name} 
			WHERE registered_date=(
                SELECT registered_date
                FROM {self._table_name}
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
	    	ORDER BY comp_rating DESC
			LIMIT ?"""
		
		query_params = (limit, )
		result = cur.execute(query, query_params)
		return [
			self._create_model_from_row(row)
			for row in result
		]

	def get_appereances_count_for_each_symbol(
		self,
		limit: Optional[int] = 100
	) -> List[SymbolAppearancesCount]:
		cur = self._db_conn.cursor()
		query = f"""SELECT 
					symbol,
					name,
					COUNT(*) 
				FROM {self._table_name} 
				GROUP BY symbol
				ORDER BY COUNT(*) DESC
				LIMIT ?"""
		
		query_params = (limit, )
		result = cur.execute(query, query_params)
		return [
			SymbolAppearancesCount(
				symbol=row[0],
				name=row[1],
				count=row[2]
			)
			for row in result
		]

	def search_by_symbol(self, symbol: str) -> Optional[List[CompositeStock]]:
		cur = self._db_conn.cursor()
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
			FROM {self._table_name} 
			WHERE symbol=?
			ORDER BY registered_date_ts DESC"""
		
		query_params = (symbol, )
		result = cur.execute(query, query_params)
		return [
			self._create_model_from_row(row)
			for row in result
		]
