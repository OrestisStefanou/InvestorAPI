from typing import Tuple, Any, List
import datetime as dt

from app.domain.time_series import IndexTimeSeriesEntry
from app.domain.price import Price
from app.domain.date import Date
from app.domain.world_index import WorldIndex
from app.repos.sql_repo import SqlRepo

class WorldIndicesTimeSeriesRepo(SqlRepo):
    """
    Repo for world_indices_time_series table
    """
    @classmethod
    def _create_row_tuple_from_model(cls, index_name: str, time_serie: IndexTimeSeriesEntry) -> Tuple[Any]:
        return (
            index_name,
            time_serie.open_price.value,
            time_serie.high_price.value,
            time_serie.low_price.value,
            time_serie.close_price.value,
            time_serie.volume,
            time_serie.registered_date.date_string,
            time_serie.registered_date.date_ts
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> IndexTimeSeriesEntry:
        registered_date_obj = dt.datetime.strptime(row[6], "%d-%m-%Y")
        return IndexTimeSeriesEntry(
            registered_date=Date(
                day=registered_date_obj.day,
                month=registered_date_obj.month,
                year=registered_date_obj.year
            ),
            open_price=Price(row[1]),
            high_price=Price(row[2]),
            low_price=Price(row[3]),
            close_price=Price(row[4]),
            volume=float(row[5])
        )
    
    @classmethod
    def add_or_replace_time_series_for_index(cls, index: WorldIndex, time_series: List[IndexTimeSeriesEntry]):
        """
        Add time series for index. This function will overwrite existing
        time series for given index if they exist
        """
        with cls._db_conn as con:
            con.execute("DELETE FROM world_indices_time_series WHERE index_name = ?", (index.value, ))
            con.executemany(
                f"INSERT INTO world_indices_time_series VALUES(?,?,?,?,?,?,?,?)",
                [
                    cls._create_row_tuple_from_model(index_name=index.value, time_serie=time_serie)
                    for time_serie in time_series
                ]
            )

    @classmethod
    def get_index_time_series(cls, index: WorldIndex) -> List[IndexTimeSeriesEntry]:
        cur = cls._db_conn.cursor()
        query = """SELECT
            index_name,
            open_price,
            high_price,
            low_price,
            close_price,
            volume,
            registered_date,
            registered_date_ts
        FROM world_indices_time_series
        WHERE index_name=?
        ORDER BY registered_date_ts DESC
        """

        query_params = (index.value, )
        result = cur.execute(query, query_params)
        return [
            cls._create_model_from_row(row)
            for row in result
        ]
