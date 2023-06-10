from functools import lru_cache, wraps
from datetime import datetime, timedelta

class BaseService:
    def __init__(self, db_session = None) -> None:
        """
        :db_session -> A database connection object
        """
        self._db_session = db_session


def timed_lru_cache(minutes: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(minutes=minutes)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache