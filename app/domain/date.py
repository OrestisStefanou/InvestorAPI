from datetime import datetime

from app.errors.domain import InvalidDateError


class Date(object):
    """
    Date string representation
    with format dd-mm-yyyy
    """
    def __init__(self, day:int, month:int, year:int):
        try:
            self._date_string = datetime(day=day, month=month, year=year).strftime("%d-%m-%Y")
            self._date_ts = datetime(day=day, month=month,year=year).timestamp()
        except ValueError:
            raise InvalidDateError()

    @property
    def date_string(self) -> str:
        return self._date_string
    
    @property
    def date_ts(self) -> float:
        return self._date_ts
