from typing import Tuple, Any, Optional

from app.repos.sql_repo import SqlRepo
from app.domain.date import Date
from app.domain.stock_overview import StockOverview

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
            stock_overview.sector,
            stock_overview.industry,
            stock_overview.market_cap,
            stock_overview.ebitda,
            stock_overview.pe_ratio,
            stock_overview.forward_pe_ratio,
            stock_overview.trailing_pe_ratio,
            stock_overview.peg_ratio,
            stock_overview.book_value,
            stock_overview.divided_per_share,
            stock_overview.dividend_yield,
            stock_overview.eps,
            stock_overview.diluted_eps,
            stock_overview.revenue_per_share,
            stock_overview.profit_margin,
            stock_overview.operating_margin,
            stock_overview.return_on_assets,
            stock_overview.return_on_equity,
            stock_overview.revenue,
            stock_overview.gross_profit,
            stock_overview.quarterly_earnings_growth_yoy,
            stock_overview.quarterly_revenue_growth_yoy,
            stock_overview.target_price,
            stock_overview.beta,
            stock_overview.price_to_sales_ratio,
            stock_overview.price_to_book_ratio,
            stock_overview.ev_to_revenue,
            stock_overview.ev_to_ebitda,
            stock_overview.outstanding_shares,
            date.date_string,
            date.date_ts
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> StockOverview:
        return StockOverview(
            symbol=row[0],
            sector=row[1],
            industry=row[2],
            market_cap=row[3],
            ebitda=row[4],
            pe_ratio=row[5],
            forward_pe_ratio=row[6],
            trailing_pe_ratio=row[7],
            peg_ratio=row[8],
            book_value=row[9],
            divided_per_share=row[10],
            dividend_yield=row[11],
            eps=row[12],
            diluted_eps=row[13],
            revenue_per_share=row[14],
            profit_margin=row[15],
            operating_margin=row[16],
            return_on_assets=row[17],
            return_on_equity=row[18],
            revenue=row[19],
            gross_profit=row[20],
            quarterly_earnings_growth_yoy=row[21],
            quarterly_revenue_growth_yoy=row[22],
            target_price=row[23],
            beta=row[24],
            price_to_sales_ratio=row[25],
            price_to_book_ratio=row[26],
            ev_to_revenue=row[27],
            ev_to_ebitda=row[28],
            outstanding_shares=29
        )
    
    def add_stock_overview_for_date(
        self,
        date: Date,
        stock_overview: StockOverview
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO stock_overview VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                industry,
                market_cap,
                ebitda,
                pe_ratio,
                forward_pe_ratio,
                trailing_pe_ratio,
                peg_ratio,
                book_value,
                divided_per_share,
                dividend_yield,
                eps,
                diluted_eps,
                revenue_per_share,
                profit_margin,
                operating_margin,
                return_on_assets,
                return_on_equity,
                revenue,
                gross_profit,
                quarterly_earnings_growth_yoy,
                quarterly_revenue_growth_yoy,
                target_price,
                beta,
                price_to_sales_ratio,
                price_to_book_ratio,
                ev_to_revenue,
                ev_to_ebitda,
                outstanding_shares,
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
