from app.repos.stock_leaders_repo import StockLeadersRepo

class ReitLeadersRepo(StockLeadersRepo):
    """
    Repo for reit_leaders table.
    """
    _table_name = 'reit_leaders'
