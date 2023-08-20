from typing import Tuple, Any, List
import datetime as dt

from app.domain.time_series import StockTimeSeriesEntry
from app.domain.price import Price
from app.domain.date import Date
from app.repos.sql_repo import SqlRepo

class StockTimeSeriesRepo(SqlRepo):
    """
    Repo for stock_time_series table
    """
    @classmethod
    def _create_row_tuple_from_model(cls, symbol: str, time_serie: StockTimeSeriesEntry) -> Tuple[Any]:
        return (
            symbol,
            time_serie.open_price.value,
            time_serie.high_price.value,
            time_serie.low_price.value,
            time_serie.close_price.value,
            time_serie.volume,
            time_serie.dividend_amount,
            time_serie.registered_date.date_string,
            time_serie.registered_date.date_ts
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> StockTimeSeriesEntry:
        registered_date_obj = dt.datetime.strptime(row[7], "%d-%m-%Y")
        return StockTimeSeriesEntry(
            registered_date=Date(
                day=registered_date_obj.day,
                month=registered_date_obj.month,
                year=registered_date_obj.year
            ),
            open_price=Price(row[1]),
            high_price=Price(row[2]),
            low_price=Price(row[3]),
            close_price=Price(row[4]),
            volume=float(row[5]),
            dividend_amount=float(row[6])
        )
    
    def add_or_replace_time_series_for_symbol(self, symbol: str, time_series: List[StockTimeSeriesEntry]):
        """
        Add time series for symbol. This function will overwrite existing
        time series for given index if they exist
        """
        with self._db_conn as con:
            con.execute("DELETE FROM stock_time_series WHERE symbol = ?", (symbol, ))
            con.executemany(
                f"INSERT INTO stock_time_series VALUES(?,?,?,?,?,?,?,?,?)",
                [
                    self._create_row_tuple_from_model(symbol=symbol, time_serie=time_serie)
                    for time_serie in time_series
                ]
            )

    def get_symbol_time_series(self, symbol: str) -> List[StockTimeSeriesEntry]:
        cur = self._db_conn.cursor()
        query = """SELECT
            symbol,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            dividend_amount,
            registered_date,
            registered_date_ts
        FROM stock_time_series
        WHERE symbol=?
        ORDER BY registered_date_ts DESC
        """

        query_params = (symbol, )
        result = cur.execute(query, query_params)
        return [
            self._create_model_from_row(row)
            for row in result
        ]
