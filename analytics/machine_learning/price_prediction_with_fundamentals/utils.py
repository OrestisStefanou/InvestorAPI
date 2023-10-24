from typing import Tuple
import datetime as dt
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


def split_data_to_train_and_test(
    df: pd.DataFrame,
    cutoff_date: dt.datetime,
    cutoff_date_column_name: str = "fiscal_date_ending"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns (train_set_df, test_set_df)
    """
    df['DateColumn'] = pd.to_datetime(df[cutoff_date_column_name])
    # Split the data into train and test based on the cutoff date
    train_set = df[df['DateColumn'] < cutoff_date].copy()
    test_set = df[df['DateColumn'] >= cutoff_date].copy()

    train_set.drop(['DateColumn',], axis=1, inplace=True)
    test_set.drop(['DateColumn',], axis=1, inplace=True)
    
    train_set = train_set.reset_index(drop=True)
    test_set = test_set.reset_index(drop=True)

    return train_set, test_set 