from app import dependencies

class SqlRepo(object):
    """
    Base class for repos that are top of sql table(s)
    """
    _db_conn = dependencies.db_conn