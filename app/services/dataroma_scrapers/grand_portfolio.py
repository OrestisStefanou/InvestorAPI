import pandas as pd

from app.http.dataroma_client import DataromaClient
from app.domain.super_investor import (
    SuperInvestorGrandPortfolioEntry,
    SuperInvestorGrandPortfolio
)

class SuperInvestorGrandPortfolioScraper:
    @classmethod
    def _scrape_grand_portfolio(cls, grand_portfolio_df: pd.DataFrame) -> list[SuperInvestorGrandPortfolioEntry]:
        grand_portfolio_records = list(grand_portfolio_df.to_records(index=False))
        grand_portfolio_records.pop()   # Remove last element because it contains next page links
        return [
            SuperInvestorGrandPortfolioEntry(
                stock=str(record[1]),
                symbol=str(record[0]),
                ownership_count=int(record[3])
            )
            for record in grand_portfolio_records
        ]

    @classmethod
    async def scrape_super_investor_grand_portfolio(cls) -> SuperInvestorGrandPortfolio:
        dataroma_client = DataromaClient()
        grand_portfolio_entries = []
        for i in range(1, 11):
            html_response = await dataroma_client.get_superinvestor_grand_portfolio(
                page_num=i
            )
            tables = pd.read_html(html_response)
            page_portfolio_entries = cls._scrape_grand_portfolio(tables[0])
            grand_portfolio_entries += page_portfolio_entries
        
        return SuperInvestorGrandPortfolio(
            portfolio=grand_portfolio_entries
        )