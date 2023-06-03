from typing import Any, List, Optional, Tuple

from app.domain.comp_rating import CompRating
from app.domain.tech_leader_stock import TechLeaderStock
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.date import Date
from app.domain.symbol_appearances_count import SymbolAppearancesCount
from app.repos.sql_repo import SqlRepo


class TechLeadersStocksRepo(SqlRepo):
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
    
    def add_tech_leaders_stocks_for_date(
        self,
        date: Date,
        data: List[TechLeaderStock]
    ) -> None:
        with self._db_conn as con:
            con.executemany(
                f"INSERT INTO tech_leaders VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                [self._create_row_tuple_from_model(tech_leader, date) for tech_leader in data]
            )

    def get_tech_leaders_stocks_for_date(
        self,
        date: Date
    ) -> Optional[List[TechLeaderStock]]:
        cur = self._db_conn.cursor()
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
            self._create_model_from_row(row)
            for row in result
        ]

    def get_latest_tech_leaders_stocks(
        self
    ) -> Optional[List[TechLeaderStock]]:
        cur = self._db_conn.cursor()
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
            self._create_model_from_row(row)
            for row in result
        ]

    def get_appereances_count_for_each_symbol(
        self,
        limit: Optional[int] = 100
    ) -> List[SymbolAppearancesCount]:
        cur = self._db_conn.cursor()
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

    def search_by_symbol(self, symbol: str) -> Optional[List[TechLeaderStock]]:
        cur = self._db_conn.cursor()
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
            self._create_model_from_row(row)
            for row in result
        ]
