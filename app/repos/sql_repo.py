import sqlite3

from app import settings

class SqlRepo(object):
    """
    Base class for repos that are top of sql table(s)
    """
    def _open_db_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(
            database=settings.db_path,
            check_same_thread=False
        )

    def __init__(self, db_conn = None) -> None:
        if db_conn is None:
            db_conn = self._open_db_conn()
        
        self._db_conn = db_conn

    def __del__(self):
        self._db_conn.close()