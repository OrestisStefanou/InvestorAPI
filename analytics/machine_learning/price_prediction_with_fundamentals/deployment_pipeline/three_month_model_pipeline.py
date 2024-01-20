import datetime as dt
import sqlite3

import pandas as pd

from app import settings
from analytics.machine_learning.price_prediction_with_fundamentals import utils

class ThreeMonthModelPipeline:

    labels = ['down', 'up']
    label_mapping = {0: 'down', 1: 'up'}

    @classmethod
    def get_dataset() -> pd.DataFrame:
        db_conn = sqlite3.connect(settings.db_path)

        query = f'''
            SELECT * 
            FROM price_prediction_dataset_v3
            WHERE DATE(Date) <= date('now', '-3 months')
            ORDER BY DATE(Date)
        '''

        dataset = pd.read_sql(query, db_conn)
        dataset.dropna(inplace=True)
        db_conn.close()

        # Create categorical target
        bins = [-float('inf'), 0, float('inf')]
        dataset['price_movement'] = pd.cut(
            dataset['price_pct_change_next_three_months'],
            bins=bins,
            labels=[0, 1],
            right=False
        )

        return dataset

    @classmethod
    def split_data_to_train_and_test(dataset: pd.DataFrame, training_cutoff_date: dt.datetime):
        train_set, test_set = utils.split_data_to_train_and_test(
            df=dataset,
            cutoff_date=training_cutoff_date,
            cutoff_date_column_name='Date'
        )

        cols_to_drop = ['symbol', 'Date', 'fiscal_date_ending', 'latest_price', 'price_pct_change_next_six_months', 'price_pct_change_next_three_months', 'price_pct_change_next_month', 'price_movement']
        target_col = 'price_movement'

        y_train = train_set[target_col]
        X_train = train_set.drop(cols_to_drop, axis=1)

        y_test = test_set[target_col]
        X_test = test_set.drop(cols_to_drop, axis=1)

        return X_train, y_train, X_test, y_test

    @classmethod
    def train_model(train_set: pd.DataFrame):
        """
        This should return the model artifact(sklearn Pipeline)
        """
        pass

    @classmethod
    def test_performance(model, test_set: pd.DataFrame):
        """
        Compare the performance against the existing model
        """
        pass

    @classmethod
    def deploy_model(model):
        pass

    
    @classmethod
    def start_pipeline():
        pass