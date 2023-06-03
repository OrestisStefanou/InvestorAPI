from app import dependencies

class SqlRepo(object):
    """
    Base class for repos that are top of sql table(s)
    """
    def __init__(self, db_conn = None) -> None:
        if db_conn is None:
            db_conn = dependencies.get_db_conn()
        
        self._db_conn = db_conn
