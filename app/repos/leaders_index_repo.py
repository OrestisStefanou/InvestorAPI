import json
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

    @classmethod
    def _create_redis_key(cls, date: Date) -> str:
        return f'{cls._table_name}_{date.date_string}'


    @classmethod
    def _serialize_stock_leader(cls, stock_leader: StockLeader) -> Dict[str, Any]:
        return {
            "name": stock_leader.name,
            "symbol": stock_leader.symbol,
            "closing_price": stock_leader.closing_price.value,
            "comp_rating": stock_leader.comp_rating.rating,
            "rs_rating": stock_leader.rs_rating.rating
        }

    @classmethod
    def _deserialize_document(cls, document: Dict[str, Any]) -> StockLeader:
        return StockLeader(
            name=document.get('name'),
            symbol=document.get('symbol'),
            closing_price=Price(document.get('closing_price')),
            comp_rating=CompRating(document.get('comp_rating')),
            rs_rating=RsRating(document.get('rs_rating'))
        )

    @classmethod
    def add_stock_leaders_for_date(
        cls,
        date: Date,
        data: List[StockLeader]
    ) -> None:
        with cls._db_conn as con:
            con.executemany(
                f"INSERT INTO {cls._table_name} VALUES(?,?,?,?,?,?,?)",
                [cls._create_row_tuple_from_model(stock_leader, date) for stock_leader in data]
            )
    
    @classmethod
    def get_stock_leaders_for_date(
        cls,
        date: Date
    ) -> Optional[List[StockLeader]]:
        cur = cls._db_conn.cursor()
        result = cur.execute(
            f"""SELECT  
                comp_rating,
                rs_rating,
                stock_name,
                stock_symbol,
                price,
                registered_date
            FROM {cls._table_name} 
            WHERE registered_date=?""",
            (date.date_string, )
        ).fetchall()
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
                    stock_symbol,
                    stock_name,
                    COUNT(*) 
                FROM {cls._table_name} 
                GROUP BY stock_symbol
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
    def search_by_symbol(cls, symbol: str) -> Optional[List[StockLeader]]:
        cur = cls._db_conn.cursor()
        query =	f"""SELECT 
                comp_rating,
                rs_rating,
                stock_name,
                stock_symbol,
                price,
                registered_date 
            FROM {cls._table_name} 
            WHERE stock_symbol=?
            ORDER BY registered_date_ts DESC"""
        
        query_params = (symbol, )
        result = cur.execute(query, query_params)
        return [
            cls._create_model_from_row(row)
            for row in result
        ]

    @classmethod
    def store_stock_leaders_for_date_in_cache(
        cls,
        date: Date,
        data: List[StockLeader]
    ) -> None:
        key = cls._create_redis_key(date)
        serialized_data = [cls._serialize_stock_leader(stock) for stock in data]
        cls._set_key_value(key, json.dumps(serialized_data))


    @classmethod
    def get_stock_leaders_for_date_from_cache(
        cls,
        date: Date
    ) -> Optional[List[StockLeader]]:
        key = cls._create_redis_key(date)
        json_data = cls._get_value_by_key(key)

        if json_data is None:
            return None

        return [
            cls._deserialize_document(utility_leader)
            for utility_leader in json.loads(json_data)
        ]
