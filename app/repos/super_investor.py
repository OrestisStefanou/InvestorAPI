from typing import Tuple, Any, List

from app.repos.sql_repo import SqlRepo
from app.domain.super_investor import (
    SuperInvestor,
    SuperInvestorPortfolio,
    SuperInvestorPortfolioHolding,
    SuperInvestorPortfolioSectorAnalysisEntry
)

class SuperInvestorRepo(SqlRepo):
    @classmethod
    def _create_row_tuple_from_portfolio_holding_model(
        cls,
        super_investor: SuperInvestor,
        portfolio_holding: SuperInvestorPortfolioHolding
    ):
        return (
            super_investor.value,
            portfolio_holding.stock,
            portfolio_holding.pct_of_portfolio,
            portfolio_holding.shares,
            portfolio_holding.reported_price,
            portfolio_holding.value
        )
    
    @classmethod
    def _create_portfolio_holding_model_from_row(
        cls,
        row: Tuple[Any]
    ) -> SuperInvestorPortfolioHolding:
        return SuperInvestorPortfolioHolding(
            stock=row[1],
            pct_of_portfolio=row[2],
            shares=row[3],
            reported_price=row[4],
            value=row[5]
        )
    
    def add_super_investor_portfolio_holdings(
        self,
        super_investor: SuperInvestor,
        portfolio_holdings: List[SuperInvestorPortfolioHolding]
    ):
        with self._db_conn as con:
            con.executemany(
                f"INSERT INTO super_investor_portfolio_holding VALUES(?, ?, ?, ?, ?, ?)",
                [
                    self._create_row_tuple_from_portfolio_holding_model(
                        super_investor=super_investor,
                        portfolio_holding=portfolio_holding
                    )
                    for portfolio_holding in portfolio_holdings
                ]
            )
    
    def delete_super_investor_portfolio_holdings(
        self,
        super_investor: SuperInvestor
    ):
        with self._db_conn as con:
            con.execute(f"DELETE FROM super_investor_portfolio_holding WHERE super_investor={super_investor.value}")
    
    def get_super_investor_portfolio_holdings(
        self,
        super_investor: SuperInvestor
    ) -> List[SuperInvestorPortfolioHolding]:
        cur = self._db_conn.cursor()
        query = """
            SELECT
                stock,
                pct_of_portfolio,
                shares,
                reported_price,
                value
            FROM super_investor_portfolio_holding
            WHERE super_investor=?
        """

        query_params = (super_investor.value, )
        result = cur.execute(query, query_params)
        return [
            self._create_portfolio_holding_model_from_row(row)
            for row in result
        ]
