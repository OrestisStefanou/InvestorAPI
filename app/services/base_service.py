
class BaseService:
    def __init__(self, db_session = None) -> None:
        """
        :db_session -> A database connection object
        """
        self._db_session = db_session
