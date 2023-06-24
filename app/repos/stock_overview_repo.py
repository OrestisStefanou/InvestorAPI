from typing import Tuple, Any

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
            stock_overview.trailing_eps,
            stock_overview.forward_eps,
            stock_overview.revenue_per_share,
            stock_overview.profit_margins,
            stock_overview.operating_margins,
            stock_overview.return_on_assets,
            stock_overview.return_on_equity,
            stock_overview.revenue,
            stock_overview.gross_profit,
            stock_overview.earnings_growth,
            stock_overview.revenue_growth,
            stock_overview.target_high_price,
            stock_overview.target_low_price,
            stock_overview.target_mean_price,
            stock_overview.target_median_price,
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
            trailing_eps=row[10],
            forward_eps=row[11],
            revenue_per_share=row[12],
            profit_margins=row[13],
            operating_margins=row[14],
            return_on_assets=row[15],
            return_on_equity=row[16],
            revenue=row[17],
            gross_profit=row[18],
            earnings_growth=row[19],
            revenue_growth=row[20],
            target_high_price=row[21],
            target_low_price=row[22],
            target_mean_price=row[23],
            target_median_price=row[24]
        )
    
    def add_stock_overview_for_date(
        self,
        date: Date,
        stock_overview: StockOverview
    ):
        with self._db_conn as con:
            con.execute(
                '''
                INSERT INTO stock_overview VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', self._create_row_tuple_from_model(stock_overview, date)
            )
