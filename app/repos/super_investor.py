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
            stock=row[0],
            pct_of_portfolio=row[1],
            shares=row[2],
            reported_price=row[3],
            value=row[4]
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
            con.execute(f"DELETE FROM super_investor_portfolio_holding WHERE super_investor='{super_investor.value}'")
    
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

    def add_super_investor_portfolio_sector_analysis(
        self,
        super_investor: SuperInvestor,
        portfolio_sector_analysis: List[SuperInvestorPortfolioSectorAnalysisEntry]
    ):
        with self._db_conn as con:
            con.executemany(
                f"INSERT INTO super_investor_portfolio_sector_analysis VALUES(?, ?, ?)",
                [
                    (
                        super_investor.value,
                        sector_analysis_entry.sector_name,
                        sector_analysis_entry.sector_pct
                    )
                    for sector_analysis_entry in portfolio_sector_analysis
                ]
            )

    def delete_super_investor_portfolio_sector_analysis(
        self,
        super_investor: SuperInvestor
    ):
        with self._db_conn as con:
            con.execute(f"DELETE FROM super_investor_portfolio_sector_analysis WHERE super_investor='{super_investor.value}'")
    
    def get_super_investor_portfolio_sector_analysis(
        self,
        super_investor: SuperInvestor
    ) -> List[SuperInvestorPortfolioSectorAnalysisEntry]:
        cur = self._db_conn.cursor()
        query = """
            SELECT
                sector_name,
                sector_pct
            FROM super_investor_portfolio_sector_analysis
            WHERE super_investor=?
        """

        query_params = (super_investor.value, )
        result = cur.execute(query, query_params)
        return [
            SuperInvestorPortfolioSectorAnalysisEntry(
                sector_name=row[0],
                sector_pct=row[1]
            )
            for row in result
        ]

    def get_super_investor_portfolio(self, super_investor: SuperInvestor) -> SuperInvestorPortfolio:
        portfolio_holdings = self.get_super_investor_portfolio_holdings(super_investor)
        sector_analysis = self.get_super_investor_portfolio_sector_analysis(super_investor)
        return SuperInvestorPortfolio(
            super_investor=super_investor,
            holdings=portfolio_holdings,
            sector_analysis=sector_analysis
        )
    
    def add_super_investor_portfolio(self, super_investor_portfolio: SuperInvestorPortfolio):
        self.add_super_investor_portfolio_holdings(
            super_investor=super_investor_portfolio.super_investor,
            portfolio_holdings=super_investor_portfolio.holdings
        )
        self.add_super_investor_portfolio_sector_analysis(
            super_investor=super_investor_portfolio.super_investor,
            portfolio_sector_analysis=super_investor_portfolio.sector_analysis
        )

    def delete_super_investor_portfolio(self, super_investor: SuperInvestor):
        self.delete_super_investor_portfolio_holdings(super_investor)
        self.delete_super_investor_portfolio_sector_analysis(super_investor)
