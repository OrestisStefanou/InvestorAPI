from typing import (
    Tuple,
    Dict,
    List,
    Optional
)
import datetime as dt
import sqlite3

import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error

def get_stock_fundamental_df(
    symbol: str,
    conn: Optional[sqlite3.Connection] = None
) -> pd.DataFrame:
    if conn is None:
        conn = sqlite3.connect('/Users/orestis/MyProjects/InvestorAPI/app/database/ibd.db') # FIX THE PATH HERE

    query = f'''
        SELECT 
            income_statement.total_revenue,
            income_statement.gross_profit,
            income_statement.operating_income,
            income_statement.net_income,
            income_statement.ebitda,
            income_statement.net_interest_income,

            balance_sheet.total_assets,
            balance_sheet.total_liabilities,
            balance_sheet.total_shareholder_equity,
            balance_sheet.total_current_assets,
            balance_sheet.total_current_liabilities,
            balance_sheet.cash_and_cash_equivalents_at_carrying_value,
            balance_sheet.long_term_debt,
            balance_sheet.current_net_receivables,
            balance_sheet.inventory,
            balance_sheet.property_plant_equipment,
            
            cash_flow.operating_cashflow,
            cash_flow.capital_expenditures,
            cash_flow.cashflow_from_investment,
            cash_flow.cashflow_from_financing,
            cash_flow.dividend_payout,
            cash_flow.proceeds_from_issuance_of_long_term_debt_and_capital_securities_net,
            cash_flow.payments_for_repurchase_of_equity,
            
            stock_overview.sector,
            stock_overview.symbol,
            income_statement.fiscal_date_ending
        FROM income_statement
        INNER JOIN balance_sheet
            ON income_statement.fiscal_date_ending = balance_sheet.fiscal_date_ending  AND balance_sheet.symbol = '{symbol}'
        INNER JOIN cash_flow
            ON income_statement.fiscal_date_ending = cash_flow.fiscal_date_ending  AND cash_flow.symbol = '{symbol}'
        INNER JOIN stock_overview
            ON income_statement.symbol = stock_overview.symbol  AND stock_overview.symbol = '{symbol}'
        WHERE income_statement.symbol = '{symbol}'
        ORDER BY DATE(income_statement.fiscal_date_ending)
    '''
    stock_df = pd.read_sql(query, conn)
    
    # Drop columns with duplicated names
    stock_df = stock_df.loc[:, ~stock_df.columns.duplicated()]

    # List of columns to convert to float
    columns_to_convert = stock_df.columns.difference(
        ['symbol', 'fiscal_date_ending', 'sector']
    )

    # Convert selected columns to float
    stock_df[columns_to_convert] = stock_df[columns_to_convert].astype(float)

    # We fill NaN values with a small value because later we perform feature
    # engineering to calculate pct change and ratios and we can't divide witrh zero
    stock_df[columns_to_convert] = stock_df[columns_to_convert].fillna(0.01)
    stock_df[columns_to_convert] = stock_df[columns_to_convert].replace(0, 0.01)

    # Feature engineering
    for column in columns_to_convert:
        # arctan percentage change
        log_pct_change_column_name = f'{column}_arctan_pct_change'
        stock_df[log_pct_change_column_name] = np.arctan(stock_df[column].pct_change())

        # Plain percentage change
        pct_change_column_name = f'{column}_pct_change'
        stock_df[pct_change_column_name] = stock_df[column].pct_change()

    return stock_df


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