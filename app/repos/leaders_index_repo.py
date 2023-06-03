from typing import Any, Dict, List, Optional, Tuple

from app.domain.stock_leader import StockLeader
from app.domain.price import Price
from app.domain.comp_rating import CompRating
from app.domain.rs_rating import RsRating
from app.domain.date import Date
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.repos.sql_repo import SqlRepo
from app.repos.redis_repo import RedisRepo

class LeadersIndexRepo(SqlRepo, RedisRepo):
    # Repos that inherit from this class must override table name
    _table_name = None

    @classmethod
    def _create_row_tuple_from_model(cls, stock_leader: StockLeader, date: Date) -> Tuple[Any]:
        return (
            stock_leader.comp_rating.rating,
            stock_leader.rs_rating.rating,
            stock_leader.name,
            stock_leader.symbol,
            stock_leader.closing_price.value,
            date.date_string,
            date.date_ts
        )

    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> StockLeader:
        return StockLeader(
            comp_rating=CompRating(row[0]),
            rs_rating=RsRating(row[1]),
            name=row[2],
            symbol=row[3],
            closing_price=Price(row[4]),
            registered_date=row[5]
        )

    def add_stock_leaders_for_date(
        self,
        date: Date,
        data: List[StockLeader]
    ) -> None:
        with self._db_conn as con:
            con.executemany(
                f"INSERT INTO {self._table_name} VALUES(?,?,?,?,?,?,?)",
                [self._create_row_tuple_from_model(stock_leader, date) for stock_leader in data]
            )

    def get_stock_leaders_for_date(
        self,
        date: Date
    ) -> Optional[List[StockLeader]]:
        cur = self._db_conn.cursor()
        result = cur.execute(
            f"""SELECT  
                comp_rating,
                rs_rating,
                stock_name,
                stock_symbol,
                price,
                registered_date
            FROM {self._table_name} 
            WHERE registered_date=?""",
            (date.date_string, )
        ).fetchall()
        return [
            self._create_model_from_row(row)
            for row in result
        ]

    def get_latest_stock_leaders(
        self,
    ) -> List[StockLeader]:
        cur = self._db_conn.cursor()
        result = cur.execute(
            f"""SELECT  
                comp_rating,
                rs_rating,
                stock_name,
                stock_symbol,
                price,
                registered_date
            FROM {self._table_name} 
            WHERE registered_date=(
                SELECT registered_date
                FROM {self._table_name}
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
            ORDER BY comp_rating DESC
            """
        ).fetchall()
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
                    stock_symbol,
                    stock_name,
                    COUNT(*) 
                FROM {self._table_name} 
                GROUP BY stock_symbol
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

    def search_by_symbol(self, symbol: str) -> Optional[List[StockLeader]]:
        cur = self._db_conn.cursor()
        query =	f"""SELECT 
                comp_rating,
                rs_rating,
                stock_name,
                stock_symbol,
                price,
                registered_date 
            FROM {self._table_name} 
            WHERE stock_symbol=?
            ORDER BY registered_date_ts DESC"""
        
        query_params = (symbol, )
        result = cur.execute(query, query_params)
        return [
            self._create_model_from_row(row)
            for row in result
        ]
