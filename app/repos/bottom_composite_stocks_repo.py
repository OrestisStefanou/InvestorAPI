from app.repos.composite_stock_repo import CompositeStockRepo

class BottomCompositeStocksRepo(CompositeStockRepo):
    _table_name = 'bottom_composite_stocks'
