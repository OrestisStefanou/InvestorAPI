import datetime as dt
import sqlite3

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import joblib

from app import settings
from analytics.machine_learning.price_prediction_with_fundamentals import utils

class BaseModelPipeline:
    def __init__(
        self,
        months: int,
        target_price_column: str,
        current_model_path: str,
        true_negative_threshold: float = 0.6,
        true_positive_threshold: float = 0.6
    ) -> None:
        self._label_mapping = {0: 'down', 1: 'up'}
        self._labels = ['down', 'up']
        self._true_negative_threshold = true_negative_threshold
        self._true_positive_threshold = true_positive_threshold
        self._months = months
        self._target_price_column = target_price_column
        self._current_model_path = current_model_path

    def get_dataset(self) -> pd.DataFrame:
        db_conn = sqlite3.connect(settings.db_path)

        query = f'''
            SELECT * 
            FROM price_prediction_dataset_v3
            WHERE DATE(Date) <= date('now', '-{self._months} months')
            ORDER BY DATE(Date)
        '''

        dataset = pd.read_sql(query, db_conn)
        dataset.dropna(inplace=True)
        db_conn.close()

        print("Latest date in dataset:", dataset['Date'].iloc[-1])
        
        # Create categorical target
        bins = [-float('inf'), 0, float('inf')]
        dataset['price_movement'] = pd.cut(
            dataset[self._target_price_column],
            bins=bins,
            labels=[0, 1],
            right=False
        )

        print("Target value counts")
        print(dataset['price_movement'].value_counts())

        return dataset

    def split_data_to_train_and_test(self, dataset: pd.DataFrame):
        today = dt.datetime.today()
        backoff_time = today - dt.timedelta(days=(self._months + 1) * 31)
        cutoff_date = dt.datetime(day=1, month=backoff_time.month, year=backoff_time.year)
        print("Cutoff date:", cutoff_date)
        train_set, test_set = utils.split_data_to_train_and_test(
            df=dataset,
            cutoff_date=cutoff_date,
            cutoff_date_column_name='Date'
        )

        cols_to_drop = ['symbol', 'Date', 'fiscal_date_ending', 'latest_price', 'price_pct_change_next_six_months', 'price_pct_change_next_three_months', 'price_pct_change_next_month', 'price_movement']
        target_col = 'price_movement'

        y_train = train_set[target_col]
        X_train = train_set.drop(cols_to_drop, axis=1)

        y_test = test_set[target_col]
        X_test = test_set.drop(cols_to_drop, axis=1)

        return X_train, y_train, X_test, y_test

    def train_model(self, X_train: pd.DataFrame, y_train: pd.DataFrame) -> Pipeline:
        """
        Train and return model artifact(sklearn Pipeline)
        """
        column_transformer = make_column_transformer(
            (
                OneHotEncoder(), ['sector']
            ),
            remainder='passthrough'
        )

        rf_three_months_classifier = make_pipeline(
            column_transformer,
            RandomForestClassifier()
        )

        rf_three_months_classifier.fit(X_train, y_train)
        return rf_three_months_classifier

    def get_current_model_performance_metrics(self, X_test: pd.DataFrame, y_test: pd.DataFrame) -> tuple[float]:
        """
        Returns existing model performance metrics(true negatives, true positives) 
        against the given test set
        """
        current_model = joblib.load(self._current_model_path)
        y_pred_current_model = current_model.predict(X_test)
        y_pred_current_model_labels = [self._label_mapping[y] for y in y_pred_current_model]
        y_test_labels = [self._label_mapping[y] for y in y_test]
        current_model_conf_matrix = confusion_matrix(
            y_true=y_test_labels,
            y_pred=y_pred_current_model_labels,
            labels=self._labels,
            normalize='true'
        )
        current_model_true_negative = current_model_conf_matrix[0][0]
        current_model_true_positive = current_model_conf_matrix[1][1]
        return (current_model_true_negative, current_model_true_positive)

    def _passes_thresholds(self, true_negatives: float, true_positives: float) -> bool:
        return true_negatives >= self._true_negative_threshold and true_positives >= self._true_positive_threshold

    def get_model_performance_metrics(
        self,
        model: Pipeline,
        X_test: pd.DataFrame,
        y_test: pd.DataFrame
    ) -> tuple[float]:
        """
        Returns the performance metrics of the model we trained in this 
        pipeline
        """
        y_test_labels = [self._label_mapping[y] for y in y_test]
        y_pred = model.predict(X_test)
        y_pred_labels = [self._label_mapping[y] for y in y_pred]
        conf_matrix = confusion_matrix(y_test_labels, y_pred_labels, labels=self._labels, normalize='true')
        true_negatives = conf_matrix[0][0]
        true_positives = conf_matrix[1][1]
        return (true_negatives, true_positives)

    def deploy_model(self, model: Pipeline):
        """
        Replace the current model with model
        """
        joblib.dump(model, self._current_model_path)

    def start_pipeline(self):
        dataset = self.get_dataset()
        X_train, y_train, X_test, y_test = self.split_data_to_train_and_test(dataset)
        new_model = self.train_model(X_train, y_train)
        new_model_true_negatives, new_model_true_positives = self.get_model_performance_metrics(
            model=new_model,
            X_test=X_test,
            y_test=y_test
        )

        current_model_true_negatives, current_model_true_positives = self.get_current_model_performance_metrics(
            X_test=X_test,
            y_test=y_test
        )

        print("New model true negatives:", new_model_true_negatives)
        print("New model true positives:", new_model_true_positives)
        print("Current model true negatives:", current_model_true_negatives)
        print("Current model true positives:", current_model_true_positives)

        if not self._passes_thresholds(
            true_negatives=new_model_true_negatives, 
            true_positives=new_model_true_positives
        ) and not self._passes_thresholds(
            true_negatives=current_model_true_negatives,
            true_positives=current_model_true_positives
        ):
            raise Exception("Both models failed to pass thresholds")
        
        if new_model_true_negatives > current_model_true_negatives and new_model_true_positives > current_model_true_positives:
            print("Deploying new model")
            self.deploy_model(new_model)
        else:
            print("Keeping current model")