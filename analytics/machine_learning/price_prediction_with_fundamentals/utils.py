import sqlite3

import pandas as pd


def get_dataset(
    db_conn = None
) -> pd.DataFrame:
    if db_conn is None:
        db_conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db')
    query = "SELECT * FROM price_prediction_dataset ORDER BY DATE(fiscal_date_ending)"

    stocks_df = pd.read_sql(query, db_conn)
    db_conn.close()

    return stocks_df
