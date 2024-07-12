from typing import List, Dict, Any

from app import dependencies

class SqlRepo(object):
    """
    Base class for repos that are top of sql table(s)
    """
    def __init__(self, db_conn = None) -> None:
        if db_conn is None:
            db_conn = dependencies.get_db_conn()
        
        self._db_conn = db_conn

    def get_database_context(self) -> List[Dict[str, Any]]:
        """
        Returns a list of dictionaries that contain the
        tables names and table column names.
        Example response:
        [
            {
                "table_name": "table_a",
                "table_columns": ["column_a", "column_b"]
            }
        ]
        """
        cur = self._db_conn.cursor()

        # Get the list of tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        # Extract table names from the result
        table_names = [table[0] for table in tables]

        database_context = []
        # Get the columns for each table
        for table in table_names:
            cur.execute(f"PRAGMA table_info({table});")
            columns = cur.fetchall()
            column_names = [column[1] for column in columns]
            database_context.append({
                "table_name": table,
                "table_columns": column_names
            })

        return database_context
