import json
from typing import Any, Dict, List, Optional, Tuple

from app.domain.comp_rating import CompRating
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.date import Date
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.repos.sql_repo import SqlRepo
from app.repos.redis_repo import RedisRepo


class TechLeadersStocksRepo(SqlRepo, RedisRepo):
    """
    Repo for tech_leaders table.
    """
    @classmethod
    def _create_row_tuple_from_model(cls, tech_leader: TechLeaderStock, date: Date) -> Tuple[Any]:
        return (
            tech_leader.comp_rating.rating,
            tech_leader.eps_rating.rating,
            tech_leader.rs_rating.rating,
            tech_leader.name,
            tech_leader.symbol,
            tech_leader.price.value,
            tech_leader.annual_eps_change_pct.value,
            tech_leader.last_qtr_eps_change_pct.value,
            tech_leader.next_qtr_eps_change_pct.value,
            tech_leader.last_qtr_sales_change_pct.value,
            tech_leader.return_on_equity,
            date.date_string,
            date.date_ts
        )

    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> TechLeaderStock:
        return TechLeaderStock(
            comp_rating=CompRating(row[0]),
            eps_rating=EpsRating(row[1]),
            rs_rating=RsRating(row[2]),
            name=row[3],
            symbol=row[4],
            price=Price(row[5]),
            annual_eps_change_pct=Percentage(row[6]),
            last_qtr_eps_change_pct=Percentage(row[7]),
            next_qtr_eps_change_pct=Percentage(row[8]),
            last_qtr_sales_change_pct=Percentage(row[9]),
            return_on_equity=row[10],
            registered_date=row[11]
        )

    @classmethod
    def _serialize_composite_stock(cls, tech_leader_stock: TechLeaderStock) -> Dict[str, Any]:
        return {
            "name": tech_leader_stock.name,
            "symbol": tech_leader_stock.symbol,
            "eps_rating": tech_leader_stock.eps_rating.rating,
            "rs_rating": tech_leader_stock.rs_rating.rating,
            "price": tech_leader_stock.price.value,
            "comp_rating": tech_leader_stock.comp_rating.rating,
            "annual_eps_change_pct": tech_leader_stock.annual_eps_change_pct.value,
            "last_qtr_eps_change_pct": tech_leader_stock.last_qtr_eps_change_pct.value,
            "next_qtr_eps_change_pct": tech_leader_stock.next_qtr_eps_change_pct.value,
            "last_qtr_sales_change_pct": tech_leader_stock.last_qtr_sales_change_pct.value,
            "return_on_equity": tech_leader_stock.return_on_equity
        }

    @classmethod
    def _deserialize_document(cls, document: Dict[str, Any]) -> TechLeaderStock:
        return TechLeaderStock(
            comp_rating=CompRating(document.get('comp_rating')),
            eps_rating=EpsRating(document.get('eps_rating')),
            rs_rating=RsRating(document.get('rs_rating')),
            name=document.get('name'),
            symbol=document.get('symbol'),
            price=Price(document.get('price')),
            annual_eps_change_pct=Percentage(document.get('annual_eps_change_pct')),
            last_qtr_eps_change_pct=Percentage(document.get('last_qtr_eps_change_pct')),
            next_qtr_eps_change_pct=Percentage(document.get('next_qtr_eps_change_pct')),
            last_qtr_sales_change_pct=Percentage(document.get('last_qtr_sales_change_pct')),
            return_on_equity=document.get('return_on_equity')
        )

    @classmethod
    def _create_redis_key(cls, date: Date):
        return f'tech_leaders_stocks_{date.date_string}'
    
    @classmethod
    def add_tech_leaders_stocks_for_date(
        cls,
        date: Date,
        data: List[TechLeaderStock]
    ) -> None:
        with cls._db_conn as con:
            con.executemany(
                f"INSERT INTO tech_leaders VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                [cls._create_row_tuple_from_model(tech_leader, date) for tech_leader in data]
            )

    @classmethod
    def get_tech_leaders_stocks_for_date(
        cls,
        date: Date
    ) -> Optional[List[TechLeaderStock]]:
        cur = cls._db_conn.cursor()
        query = """SELECT 
                    comp_rating,
                    eps_rating,
                    rs_rating,
                    stock_name,
                    stock_symbol,
                    price,
                    annual_eps_change_pct,
                    last_qtr_eps_change_pct,
                    next_qtr_eps_change_pct,
                    last_qtr_sales_change_pct,
                    return_on_equity,
                    registered_date
                FROM tech_leaders 
                WHERE registered_date=?"""
        query_params = (date.date_string, )
        result = cur.execute(query, query_params)
        return [
            cls._create_model_from_row(row)
            for row in result
        ]

    @classmethod
    def get_latest_tech_leaders_stocks(
        cls
    ) -> Optional[List[TechLeaderStock]]:
        cur = cls._db_conn.cursor()
        query = """SELECT 
                    comp_rating,
                    eps_rating,
                    rs_rating,
                    stock_name,
                    stock_symbol,
                    price,
                    annual_eps_change_pct,
                    last_qtr_eps_change_pct,
                    next_qtr_eps_change_pct,
                    last_qtr_sales_change_pct,
                    return_on_equity,
                    registered_date
                FROM tech_leaders 
                WHERE registered_date=(
                    SELECT registered_date
                    FROM tech_leaders
                    ORDER BY registered_date_ts DESC
                    LIMIT 1
                )
	    	    ORDER BY comp_rating DESC"""
        result = cur.execute(query)
        return [
            cls._create_model_from_row(row)
            for row in result
        ]

    @classmethod
    def get_appereances_count_for_each_symbol(
        cls,
        limit: Optional[int] = 100
    ) -> List[SymbolAppearancesCount]:
        cur = cls._db_conn.cursor()
        query = """SELECT 
                    stock_symbol,
                    stock_name,
                    COUNT(*) 
                FROM tech_leaders
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

    @classmethod
    def search_by_symbol(cls, symbol: str) -> Optional[List[TechLeaderStock]]:
        cur = cls._db_conn.cursor()
        query =	f"""SELECT 
                comp_rating,
                eps_rating,
                rs_rating,
                stock_name,
                stock_symbol,
                price,
                annual_eps_change_pct,
                last_qtr_eps_change_pct,
                next_qtr_eps_change_pct,
                last_qtr_sales_change_pct,
                return_on_equity,
                registered_date 
            FROM tech_leaders 
            WHERE stock_symbol=?
            ORDER BY registered_date_ts DESC"""
        
        query_params = (symbol, )
        result = cur.execute(query, query_params)
        return [
            cls._create_model_from_row(row)
            for row in result
        ]

    @classmethod
    def store_tech_leaders_stocks_for_date_in_cache(
        cls,
        date: Date,
        data: List[TechLeaderStock]
    ) -> None:
        key = cls._create_redis_key(date)
        serialized_data = [cls._serialize_composite_stock(stock) for stock in data]
        cls._set_key_value(key, json.dumps(serialized_data))

    @classmethod
    def get_tech_leaders_stocks_for_date_from_cache(
        cls,
        date: Date
    ) -> Optional[List[TechLeaderStock]]:
        key = cls._create_redis_key(date)
        json_data = cls._get_value_by_key(key)

        if json_data is None:
            return None

        return [
            cls._deserialize_document(stock)
            for stock in json.loads(json_data)
        ]
