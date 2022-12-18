from app.repos.stock_leaders_repo import StockLeadersRepo

class DividendLeadersRepo(StockLeadersRepo):
    """
    Repo for dividend_leaders table.
    """
    _table_name = 'dividend_leaders'