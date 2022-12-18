from app.repos.stock_leaders_repo import StockLeadersRepo

class UtilityLeadersRepo(StockLeadersRepo):
    """
    Repo for utility_leaders table.
    """
    _table_name = 'utility_leaders'
