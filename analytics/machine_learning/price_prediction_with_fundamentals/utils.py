from typing import (
    Tuple,
    Optional,
    Dict,
    List
)
import datetime as dt
import sqlite3

import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    OneHotEncoder,
    MinMaxScaler,
    StandardScaler
)
from sklearn.metrics import mean_absolute_percentage_error

from analytics.machine_learning.utils import preprocessing


def get_features(
    db_conn = None,
    features_categories: List[str] = None,
    target: str = 'price_pct_change_next_three_months'
) -> pd.DataFrame:
    """
    Params:
        - db_conn: Database connection object
        - features_cagories: A list with the categories of features to keep.
            Available feature categories: 'arctan_ratio', 'arctan_pct_change', 'pct_change'
        - target: Name of the target column
            Available targets: 'avg_next_three_months_price', 'price_pct_change_next_three_months'
    """
    if db_conn is None:
        db_conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db')

    query = '''
        SELECT * 
        FROM price_prediction_features
        WHERE DATE(fiscal_date_ending) <= date('now', '-3 months')
        ORDER BY DATE(fiscal_date_ending)
    '''

    features_df = pd.read_sql(query, db_conn)
    db_conn.close()

    # Drop rows that contain null values
    columns_with_null = features_df.columns[features_df.isna().any()].tolist()
    features_df.dropna(subset=columns_with_null, inplace=True)
    features_df.reset_index(inplace=True, drop=True)

    if features_categories:
        valid_feature_categories = ['arctan_ratio', 'arctan_pct_change', 'pct_change']
        invalid_categories = [category for category in features_categories if category not in valid_feature_categories]
        if invalid_categories:
            raise ValueError(f"Available categories are: {', '.join(valid_feature_categories)}")

        columns_to_keep = [
            'symbol', 
            'sector', 
            'fiscal_date_ending', 
            'avg_interest_rate', 
            'avg_treasury_yield',
            'avg_unemployment_rate',
            'avg_global_commodities_index_value',
            'avg_oil_price',
            'avg_natural_gas_price',
            'inflation',
            'price_volatility_three_months',
        ]

        if target == 'price_pct_change_next_three_months':
            columns_to_keep = columns_to_keep + ['price_pct_change_three_months', 'price_pct_change_next_three_months']
        else:
            columns_to_keep = columns_to_keep + ['avg_three_months_price', 'avg_next_three_months_price']

        for col_name in features_df.columns:
            for category in features_categories:
                if str(col_name).endswith(f'_{category}'):
                    if category == 'pct_change' and str(col_name).endswith(f'_arctan_pct_change'):
                        continue

                    columns_to_keep.append(col_name)

        return features_df[columns_to_keep]

    return features_df


def get_dataset(
    db_conn = None,
) -> pd.DataFrame:
    if db_conn is None:
        db_conn = sqlite3.connect('/home/orestis/code/Orestis/InvestorAPI/app/database/ibd.db')

    query = '''
        SELECT * 
        FROM price_prediction_dataset 
        WHERE DATE(fiscal_date_ending) <= date('now', '-3 months')
        ORDER BY DATE(fiscal_date_ending)
    '''

    stocks_df = pd.read_sql(query, db_conn)
    db_conn.close()

    # Drop rows that contain null values
    columns_with_null = stocks_df.columns[stocks_df.isna().any()].tolist()
    stocks_df.dropna(subset=columns_with_null, inplace=True)
    stocks_df.reset_index(inplace=True, drop=True)

    world_indices_value_change_cols = [
        's_p_500_index_value_change',
        'dow_jones_index_value_change',
        'nasdaq_index_value_change',
        'nyse_index_value_change'
    ]

    economic_indicators_avg_value_cols = [
        'avg_interest_rate',
        'avg_treasury_yield',
        'avg_natural_gas_price',
        'avg_oil_price',
        'avg_unemployment_rate',
        'avg_global_commodities_index_value',
        'inflation'
    ]

    economic_indicators_value_change_cols = [
        'interest_rate_value_change',
        'treasury_yield_value_change',
        'natural_gas_price_value_change',
        'oil_price_value_change',
        'unemployment_rate_value_change',
        'global_commodities_index_value_change',
    ]


    value_change_cols = ['change_in_cash_and_cash_equivalents', 'change_in_exchange_rate']
    for col_name in stocks_df.columns:
        if '_value_change' in col_name:
            if col_name not in world_indices_value_change_cols and col_name not in economic_indicators_value_change_cols:
                value_change_cols.append(col_name)


    columnss_to_keep = value_change_cols + economic_indicators_avg_value_cols + ['symbol', 'fiscal_date_ending', 'sector', 'avg_three_months_price', 'avg_next_three_months_price']

    return stocks_df[columnss_to_keep]


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
    scaler: Optional[MinMaxScaler | StandardScaler] = None,
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

    if scaler:
        float_columns = X.select_dtypes(include=['float64'])
        columns_to_scale = list(float_columns.columns)

        scaled_train_set = preprocessing.perform_scaling(
            df=one_hot_encoded_train_set,
            scaler=scaler,
            fit=True,
            columns_to_scale=columns_to_scale
        )
        return scaled_train_set.reset_index(drop=True)

    return one_hot_encoded_train_set


def tranform_target(
    y: pd.Series,
    scaler: MinMaxScaler,
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
    return preprocessing.scale_transformation_on_target(
        target=y,
        scaler=scaler,
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


def calculate_avg_pct_loss_per_sector(
    y_pred: pd.Series,
    y_actual: pd.Series,
    sector_series: pd.Series
) -> Dict[str, float]:
    predictions_per_sector: Dict[str, List] = dict()
    actual_values_per_sector: Dict[str, List] = dict()

    for i in range(len(y_pred)):
        sector = sector_series[i]
        if sector in predictions_per_sector:
            predictions_per_sector[sector].append(y_pred[i])
            actual_values_per_sector[sector].append(y_actual[i])
        else:
            predictions_per_sector[sector] = [y_pred[i], ]
            actual_values_per_sector[sector] = [y_actual[i], ]
    
    avg_pct_loss_per_sector = dict()
    for sector in predictions_per_sector:
        avg_pct_loss_per_sector[sector] = mean_absolute_percentage_error(
            y_true=actual_values_per_sector[sector],
            y_pred=predictions_per_sector[sector]
        )

    return avg_pct_loss_per_sector


def calculate_avg_pct_loss_per_price_bucket(
    y_pred: pd.Series,
    y_actual: pd.Series,
    buckets: List[Tuple[float, float]]
):
    def get_price_bucket(price: float) -> int:
        """
        Returns the bucket index that the price belongs to or
        -1 in case the price doesn't belong to any bucket
        """
        for i in range(len(buckets)):
            if price > buckets[i][0] and price < buckets[i][1]:
                return i

        return -1

    def create_string_key_for_bucket(bucket_index: int) -> str:
        if bucket_index == -1:
            return f"{buckets[bucket_index][1]}+"

        return f"{buckets[bucket_index][0]} - {buckets[bucket_index][1]}"

    bucket_total_pct_loss_dict = dict()
    bucket_pred_count_dict = dict()
    for i in range(len(y_pred)):
        pct_loss = (abs(y_pred[i] - y_actual[i]) / y_pred[i]) * 100
        bucket_index = get_price_bucket(y_actual[i])
        bucket_name = create_string_key_for_bucket(bucket_index)
        if bucket_name in bucket_total_pct_loss_dict:
            bucket_total_pct_loss_dict[bucket_name] += pct_loss
            bucket_pred_count_dict[bucket_name] += 1
        else:
            bucket_total_pct_loss_dict[bucket_name] = pct_loss
            bucket_pred_count_dict[bucket_name] = 1
    
    avg_pct_loss_per_bucket_dict = dict() 
    for bucket in bucket_total_pct_loss_dict:
        avg_pct_loss_per_bucket_dict[bucket] = bucket_total_pct_loss_dict[bucket] / bucket_pred_count_dict[bucket]

    return avg_pct_loss_per_bucket_dict


def get_feature_importance_sorted(
    feature_importance_scores: List[float],
    feature_names: List[str]
) -> List[Tuple[str, float]]:
    feature_name_with_score_list = list()
    for i in range(len(feature_importance_scores)):
        feature_name = feature_names[i]
        feature_name_with_score_list.append((feature_name, feature_importance_scores[i]))
    
    return sorted(feature_name_with_score_list, key=lambda x: x[1], reverse=True)


def get_high_prob_predictions_with_ground_truth_labels(
    predicted_probabilities: np.ndarray,
    y_pred: np.ndarray,
    y_test: np.ndarray,
    threshold: float = 0.7
):
    """
    Returns the predictions along with the ground truth labels
    only for the predictions where the predicted probability is
    higher than the threshold
    Returns: (y_pred_high_prob, y_test)
    """
    high_probability_predictions = []
    ground_truth_labels =[]
    for i in range(len(y_pred)):
        predicted_label = y_pred[i]
        predicted_probability = predicted_probabilities[i][predicted_label]
        if predicted_probability >= threshold:
            high_probability_predictions.append(predicted_label)
            ground_truth_labels.append(y_test[i])
        else:
            continue
    
    return high_probability_predictions, ground_truth_labels