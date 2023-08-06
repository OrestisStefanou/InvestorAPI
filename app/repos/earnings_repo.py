from typing import Tuple, Any, Optional, List

from app.repos.sql_repo import SqlRepo
from app.domain.earnings import Earnings

class EarningsRepo(SqlRepo):
    """
    Repo for earnings table
    """
    @classmethod
    def _create_row_tuple_from_model(
        cls,
        earnings: Earnings,
    ) -> Tuple[Any]:
        return (
            earnings.symbol,
            earnings.fiscal_date_ending,
            earnings.reported_date,
            earnings.reported_eps,
            earnings.estimated_eps,
            earnings.surprise,
            earnings.surprise_percentage,
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> Earnings:
        return Earnings(
            symbol=row[0],
            fiscal_date_ending=row[1],
            reported_date=row[2],
            reported_eps=row[3],
            estimated_eps=row[4],
            surprise=row[5],
            surprise_percentage=row[6]
        )
    
    def add_earnings(
        self,
        earnings: Earnings
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO earnings VALUES (? ,? ,? ,?, ?, ?, ?)
                ''', self._create_row_tuple_from_model(earnings)
            )

    def get_earnings_for_symbol(
        self,
        symbol: str,
    ) -> Optional[List[Earnings]]:
        cur  = self._db_conn.cursor()
        query = '''
            SELECT
                symbol,
                fiscal_date_ending,
                reported_date,
                reported_eps,
                estimated_eps,
                surprise,
                surprise_percentage
            FROM earnings
            WHERE symbol = ?
        '''

        query_params = (symbol, )
        rows = cur.execute(query, query_params).fetchall()
        
        if len(rows) == 0:
            return None
         
        return [
            self._create_model_from_row(row)
            for row in rows
        ]

    def delete_earnings_of_symbol(self, symbol: str) -> None:
        with self._db_conn as con:
            con.execute(
                '''
                DELETE FROM earnings WHERE symbol = ?
                ''', (symbol, )
            )
