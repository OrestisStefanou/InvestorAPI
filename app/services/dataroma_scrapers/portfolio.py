import pandas as pd

from app.http.dataroma_client import DataromaClient
from app.domain.super_investor import (
    SuperInvestor,
    SuperInvestorPortfolioHolding,
    SuperInvestorPortfolio,
    SuperInvestorPortfolioSectorAnalysisEntry
)

class SuperInvestorPortfolioScraper:
    @classmethod
    def _convert_portfolio_holding_table_record_to_domain_model(cls, record) -> SuperInvestorPortfolioHolding:
        return SuperInvestorPortfolioHolding(
            stock=str(record[1]),
            pct_of_portfolio=float(record[2]),
            shares=float(record[4]),
            reported_price=str(record[5]),
            value=str(record[6])
        )
    
    @classmethod
    def _scrape_portfolio_holdings(cls, holdings_df: pd.DataFrame) -> list[SuperInvestorPortfolioHolding]:
        portfolio_holdings_records = holdings_df.to_records(index=False)
        return [
            cls._convert_portfolio_holding_table_record_to_domain_model(
                record=record
            )
            for record in portfolio_holdings_records
        ]

    @classmethod
    def _scrape_portfolio_sector_analysis(cls, sector_analysis_df: pd.DataFrame) -> list[SuperInvestorPortfolioSectorAnalysisEntry]:
        sector_analysis_records = sector_analysis_df.to_records(index=False)
        return [
            SuperInvestorPortfolioSectorAnalysisEntry(
                sector_name=str(record[0]),
                sector_pct=float(record[1])
            )
            for record in sector_analysis_records
        ]

    @classmethod
    async def scrape_super_investor_portfolio(cls, super_investor: SuperInvestor) -> SuperInvestorPortfolio:
        dataroma_client = DataromaClient()
        html_response = await dataroma_client.get_superinvestor_portfolio(
            super_investor=super_investor
        )

        tables = pd.read_html(html_response)
        portfolio_holdings = cls._scrape_portfolio_holdings(tables[0])
        sector_analysis = cls._scrape_portfolio_sector_analysis(tables[1])

        return SuperInvestorPortfolio(
            super_investor=super_investor,
            holdings=portfolio_holdings,
            sector_analysis=sector_analysis
        )
