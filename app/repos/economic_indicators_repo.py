from typing import Tuple, Any, List
import datetime as dt

from app.domain.time_series import EconomicIndicatorTimeSeriesEntry
from app.domain.price import Price
from app.domain.date import Date
from app.domain.economic_indicator import EconomicIndicator
from app.repos.sql_repo import SqlRepo

class EconomicIndicatorTimeSeriesRepo(SqlRepo):
    """
    Repo for economic_indicator_time_series table
    """
    @classmethod
    def _create_row_tuple_from_model(cls, indicator: str, time_serie: EconomicIndicatorTimeSeriesEntry) -> Tuple[Any]:
        return (
            indicator,
            time_serie.value.value,
            time_serie.unit,
            time_serie.registered_date.date_string,
            time_serie.registered_date.date_ts
        )
    
    @classmethod
    def _create_model_from_row(cls, row: Tuple[Any]) -> EconomicIndicatorTimeSeriesEntry:
        registered_date_obj = dt.datetime.strptime(row[3], "%d-%m-%Y")
        return EconomicIndicatorTimeSeriesEntry(
            registered_date=Date(
                day=registered_date_obj.day,
                month=registered_date_obj.month,
                year=registered_date_obj.year            
            ),
            value=Price(row[1]),
            unit=row[2]
        )
    
    @classmethod
    def add_or_replace_time_series_for_indicator(
        cls,
        indicator: EconomicIndicator,
        time_series: List[EconomicIndicatorTimeSeriesEntry]        
    ):
        """
        Add time series for indicator. This function will overwrite existing
        time series for given indicator if they exist
        """
        with cls._db_conn as con:
            con.execute("DELETE FROM economic_indicator_time_series WHERE indicator_name = ?", (indicator.value, ))
            con.executemany(
                f"INSERT INTO economic_indicator_time_series VALUES(?,?,?,?,?)",
                [
                    cls._create_row_tuple_from_model(indicator=indicator.value, time_serie=time_serie)
                    for time_serie in time_series
                ]
            )

    @classmethod
    def get_indicator_time_series(cls, indicator: EconomicIndicator) -> List[EconomicIndicatorTimeSeriesEntry]:
        cur = cls._db_conn.cursor()
        query = """SELECT
            indicator_name,
            value,
            unit,
            registered_date,
            registered_date_ts
        FROM economic_indicator_time_series
        WHERE indicator_name=?
        ORDER BY registered_date_ts DESC
        """

        query_params = (indicator.value, )
        result = cur.execute(query, query_params)
        return [
            cls._create_model_from_row(row)
            for row in result
        ]
