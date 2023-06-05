from typing import Any, List, Optional, Tuple

from app.domain.acc_dis_rating import AccDisRating
from app.domain.price import Price
from app.domain.percentage import Percentage
from app.domain.comp_rating import CompRating
from app.domain.composite_stock import CompositeStock
from app.domain.date import Date
from app.domain.eps_rating import EpsRating
from app.domain.rs_rating import RsRating
from app.domain.sector_performance import SectorPerformance, SectorPriceChangePct
from app.domain.sector import Sector
from app.domain.smr_rating import SmrRating
from app.repos.sql_repo import SqlRepo


class StocksWithSectorRepo(SqlRepo):
    """
    Repo for stocks_with_sector table
    """
    @classmethod
    def _create_row_tuple_from_model(
        cls,
        composite_stock: CompositeStock,
        sector: SectorPerformance,
        date: Date
    ) -> Tuple[Any]:
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
            composite_stock.smr_rating.rating,
            sector.sector_name,
            sector.daily_price_change_pct.change_pct,
            sector.start_of_year_price_change_pct.change_pct,
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
            smr_rating=SmrRating(row[9]),
            sector=Sector(row[10]),
            registered_date=row[11],
        )

    def add_stocks_with_sector_for_date(
        self,
        date: Date,
        stocks: List[List[CompositeStock]],
        sectors: List[SectorPerformance]
    ):
        with self._db_conn as con:
            for i in range(len(sectors)):
                sector = sectors[i]
                sector_stocks = stocks[i]
                con.executemany(
                    f"INSERT INTO stocks_with_sector VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    [
                        self._create_row_tuple_from_model(stock, sector, date)
                        for stock in sector_stocks
                    ]
                )

    def get_sector_stocks(
        self,
        sector: Sector
    ) -> Optional[List[CompositeStock]]:
        cur = self._db_conn.cursor()
        query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
                smr_rating,
                sector_name,
                registered_date
			FROM stocks_with_sector 
			WHERE sector_name=? AND registered_date=(
                SELECT registered_date
                FROM stocks_with_sector
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
            ORDER BY comp_rating DESC"""
        
        query_params = (sector.value, )
    
        result = cur.execute(query,query_params).fetchall()
        return [
			self._create_model_from_row(row)
			for row in result
		]

    def get_sectors_performance(
        self,
        sector: Optional[Sector] = None
    ) -> List[SectorPerformance]:
        cur = self._db_conn.cursor()
        query = """SELECT 
                    DISTINCT sector_name,
                    sector_daily_price_change_pct,
                    sector_start_of_year_price_change_pct,
                    registered_date,
                    registered_date_ts
                FROM stocks_with_sector"""
        
        query_params = ()
        
        if sector:
            query += " WHERE sector_name = ?"
            query_params = (sector.value, )
            
        query += " ORDER BY registered_date_ts DESC"
        
        result = cur.execute(query, query_params).fetchall()
        return [
            SectorPerformance(
                sector_name=Sector(row[0]),
                daily_price_change_pct=SectorPriceChangePct(row[1], validate=False),
                start_of_year_price_change_pct=SectorPriceChangePct(row[2], validate=False),
                registered_date=row[3],
                registered_date_ts=row[4]
            )
            for row in result
        ]

    def get_stock_historical_data(
        self,
        stock_symbol: str
    ) -> Optional[List[CompositeStock]]:
        cur = self._db_conn.cursor()
        query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
                smr_rating,
                sector_name,
                registered_date
			FROM stocks_with_sector 
			WHERE symbol=?
            ORDER BY registered_date_ts DESC"""
        
        query_params = (stock_symbol, )
    
        result = cur.execute(query,query_params).fetchall()
        return [
			self._create_model_from_row(row)
			for row in result
		]

    def get_eps_rating_leaders(self) -> List[CompositeStock]:
        cur = self._db_conn.cursor()
        query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
                smr_rating,
                sector_name,
                registered_date
			FROM stocks_with_sector 
			WHERE registered_date=(
                SELECT registered_date
                FROM stocks_with_sector
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
            ORDER BY eps_rating DESC
            LIMIT 100"""
            
        result = cur.execute(query).fetchall()
        return [
			self._create_model_from_row(row)
			for row in result
		]

    def get_rs_rating_leaders(self) -> List[CompositeStock]:
        cur = self._db_conn.cursor()
        query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
                smr_rating,
                sector_name,
                registered_date
			FROM stocks_with_sector 
			WHERE registered_date=(
                SELECT registered_date
                FROM stocks_with_sector
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
            ORDER BY rs_rating DESC
            LIMIT 100"""
            
        result = cur.execute(query).fetchall()
        return [
			self._create_model_from_row(row)
			for row in result
		]

    def get_stocks_under_heavy_buying(self) -> List[CompositeStock]:
        cur = self._db_conn.cursor()
        query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
                smr_rating,
                sector_name,
                registered_date
			FROM stocks_with_sector 
			WHERE acc_dis_rating='A+'
            AND registered_date=(
                SELECT registered_date
                FROM stocks_with_sector
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
            ORDER BY eps_rating DESC
            LIMIT 100"""

        result = cur.execute(query).fetchall()
        return [
			self._create_model_from_row(row)
			for row in result
		]

    def get_stocks_under_heavy_selling(self) -> List[CompositeStock]:
        cur = self._db_conn.cursor()
        query = """SELECT 
				comp_rating,
				eps_rating,
				rs_rating,
				acc_dis_rating,
				fifty_two_wk_high,
				name,
				symbol,
				closing_price,
				vol_chg_pct,
                smr_rating,
                sector_name,
                registered_date
			FROM stocks_with_sector 
			WHERE acc_dis_rating='E'
            AND registered_date=(
                SELECT registered_date
                FROM stocks_with_sector
                ORDER BY registered_date_ts DESC
                LIMIT 1
            )
            ORDER BY eps_rating DESC
            LIMIT 100"""

        result = cur.execute(query).fetchall()
        return [
			self._create_model_from_row(row)
			for row in result
		]
