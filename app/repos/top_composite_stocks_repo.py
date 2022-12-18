from app.repos.composite_stock_repo import CompositeStockRepo

class TopCompositeStocksRepo(CompositeStockRepo):
    _table_name = 'top_composite_stocks'
