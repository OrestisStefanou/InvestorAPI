from typing import Tuple, Any, Optional

from app.repos.sql_repo import SqlRepo
from app.domain.date import Date
from app.domain.stock_overview import StockOverview
from app.domain.sector import Sector

class StockOverviewRepo(SqlRepo):
    """
    Repo for stock_overview table
    """
    @classmethod
    def _create_row_tuple_from_model(
        cls,
        stock_overview: StockOverview,
        date: Date
    ) -> Tuple[Any]:
        return (
            stock_overview.symbol,
            stock_overview.sector.value,
            stock_overview.market_cap,
            stock_overview.ebitda,
            stock_overview.forward_pe_ratio,
            stock_overview.trailing_pe_ratio,
            stock_overview.peg_ratio,
            stock_overview.book_value,
            stock_overview.divided_per_share,
            stock_overview.dividend_yield,
            stock_overview.eps,
            stock_overview.revenue_per_share,
            stock_overview.profit_margins,
            stock_overview.operating_margins,
            stock_overview.return_on_assets,
            stock_overview.return_on_equity,
            stock_overview.revenue,
            stock_overview.gross_profit,
            stock_overview.earnings_growth,
            stock_overview.revenue_growth,
            stock_overview.target_price,
            stock_overview.beta,
            stock_overview.price_to_sales_ratio,
            stock_overview.price_to_book_ratio,
            stock_overview.ev_to_revenue,
            stock_overview.ev_to_ebitda,
            date.date_string,
            date.date_ts
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> StockOverview:
        return StockOverview(
            symbol=row[0],
            sector=Sector(row[1]),
            market_cap=row[2],
            ebitda=row[3],
            forward_pe_ratio=row[4],
            trailing_pe_ratio=row[5],
            peg_ratio=row[6],
            book_value=row[7],
            divided_per_share=row[8],
            dividend_yield=row[9],
            eps=row[10],
            revenue_per_share=row[11],
            profit_margins=row[12],
            operating_margins=row[13],
            return_on_assets=row[14],
            return_on_equity=row[15],
            revenue=row[16],
            gross_profit=row[17],
            earnings_growth=row[18],
            revenue_growth=row[19],
            target_price=row[20],
            beta=row[21],
            price_to_sales_ratio=row[22],
            price_to_book_ratio=row[23],
            ev_to_revenue=row[24],
            ev_to_ebitda=row[25],
        )
    
    def add_stock_overview_for_date(
        self,
        date: Date,
        stock_overview: StockOverview
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO stock_overview VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', self._create_row_tuple_from_model(stock_overview, date)
            )

    def get_stock_overview(
        self,
        symbol: str
    ) -> Optional[StockOverview]:
        cur  = self._db_conn.cursor()
        query = '''
            SELECT
                symbol,
                sector,
                market_cap,
                ebitda,
                forward_pe_ratio,
                trailing_pe_ratio,
                peg_ratio,
                book_value,
                divided_per_share,
                dividend_yield,
                eps,
                revenue_per_share,
                profit_margins,
                operating_margins,
                return_on_assets,
                return_on_equity,
                revenue,
                gross_profit,
                earnings_growth,
                revenue_growth,
                target_price,
                beta,
                price_to_sales_ratio,
                price_to_book_ratio,
                ev_to_revenue,
                ev_to_ebitda,
                registered_date,
                registered_date_ts
            FROM stock_overview
            WHERE symbol = ?
            ORDER BY registered_date_ts DESC
            LIMIT 1
        '''

        query_params = (symbol, )
        row = cur.execute(query, query_params).fetchone()
        return self._create_model_from_row(row) if row else None
