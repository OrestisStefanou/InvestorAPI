from typing import Tuple, Optional
import datetime as dt
import sqlite3

import pandas as pd
from sklearn.preprocessing import (
    OneHotEncoder,
    MinMaxScaler
)

from analytics.machine_learning.utils import preprocessing

def get_dataset(
    db_conn = None
) -> pd.DataFrame:
    if db_conn is None:
        db_conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db')
    
    query = "SELECT * FROM price_prediction_dataset ORDER BY DATE(fiscal_date_ending)"

    stocks_df = pd.read_sql(query, db_conn)
    db_conn.close()

    # Drop rows that contain null values
    columns_with_null = stocks_df.columns[stocks_df.isna().any()].tolist()
    stocks_df.dropna(subset=columns_with_null, inplace=True)
    stocks_df.reset_index(inplace=True, drop=True)

    return stocks_df


def split_data_to_train_and_test(
    df: pd.DataFrame,
    cutoff_date: dt.datetime,
    cutoff_date_column_name: str = "fiscal_date_ending"
) -> Tuple[pd.DataFrame]:
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


def split_into_input_and_target(
    train_set: pd.DataFrame,
    test_set: pd.DataFrame
) -> Tuple[pd.DataFrame]:
    """
    Returns (X_train, y_train, X_test, y_test)
    """
    y_train = train_set['price']
    X_train = train_set.drop(['price'], axis=1)

    y_test = test_set['price']
    X_test = test_set.drop(['price'], axis=1)

    return (X_train, y_train, X_test, y_test)


def transform_input(
    X: pd.DataFrame,
    one_hot_encoder: OneHotEncoder,
    min_max_scaler: Optional[MinMaxScaler] = None,
    fit: bool = False
) -> pd.DataFrame:
    """
    Performs one hot encoding and min max scaling
    on X input set. Parameter fit should be True 
    when X param is the training set.
    """
    # Drop useless columns
    X.drop(['symbol', 'fiscal_date_ending', 'reported_currency'], axis=1, inplace=True)
    
    one_hot_encoded_train_set = preprocessing.perform_one_hot_encoding(
        df=X,
        categorical_columns=['sector'],
        encoder=one_hot_encoder,
        fit=fit
    )

    if min_max_scaler:
        float_columns = X.select_dtypes(include=['float64'])
        columns_to_scale = list(float_columns.columns)

        scaled_train_set = preprocessing.perform_min_max_scaling(
            df=one_hot_encoded_train_set,
            min_max_scaler=min_max_scaler,
            fit=True,
            columns_to_scale=columns_to_scale
        )
        return scaled_train_set.reset_index(drop=True)

    return one_hot_encoded_train_set


def tranform_target(
    y: pd.Series,
    min_max_scaler: MinMaxScaler,
    inverse: bool = False,
    fit: bool = False
) -> pd.Series:
    """
    Performs min max scaling on y target.
    Parameter fit should be True if target is
    used for training otherwise False.
    Parameter inverse should be True in case
    that we want to transform the scaled value back
    to it's normal scale 
    """
    return preprocessing.min_max_scale_transformation_on_target(
        target=y,
        min_max_scaler=min_max_scaler,
        inverse=inverse,
        fit=fit
    )


def calculate_avg_pct_loss(
    y_pred: pd.Series,
    y_actual: pd.Series
) -> float:
    total_pct_loss = 0
    for i in range(len(y_pred)):
        pct_loss = (abs(y_pred[i] - y_actual[i]) / y_pred[i]) * 100
        total_pct_loss += pct_loss
    
    return float(total_pct_loss / len(y_pred))
