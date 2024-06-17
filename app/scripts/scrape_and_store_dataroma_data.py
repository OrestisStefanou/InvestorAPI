from app.domain.super_investor import SuperInvestor
from app.repos.super_investor import SuperInvestorRepo
from app.services.dataroma_scrapers.portfolio import SuperInvestorPortfolioScraper

async def scrape_and_store_super_investor_portfolios():
    scraper = SuperInvestorPortfolioScraper()
    repo = SuperInvestorRepo()
    for super_investor in SuperInvestor:
        portfolio = await scraper.scrape_super_investor_portfolio(super_investor)
        # Delete existing portfolio from the database
        repo.delete_super_investor_portfolio(
            super_investor=super_investor
        )
        # Add the updated one
        repo.add_super_investor_portfolio(
            super_investor_portfolio=portfolio
        )
