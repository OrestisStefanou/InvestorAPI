import datetime as dt
from typing import Dict

import joblib
import pandas as pd
import shap

from analytics.utils import (
    get_interest_rate_df,
    get_sector_time_series_df,
    get_stock_time_series_df,
    get_treasury_yield_df,
    calculate_sector_pct_change,
    calculate_time_series_pct_change,
    calculate_time_series_volatility,
    find_latest_financials_data,
    find_time_series_most_recent_value
)
from analytics.machine_learning.price_prediction_with_fundamentals.utils import (
    get_stock_fundamental_df
)

interest_rate_df = get_interest_rate_df()
treasury_yield_df = get_treasury_yield_df()

sectors_time_series = {
    'LIFE SCIENCES': get_sector_time_series_df('LIFE SCIENCES'),
    'TECHNOLOGY': get_sector_time_series_df('TECHNOLOGY'),
    'TRADE & SERVICES': get_sector_time_series_df('TRADE & SERVICES'),
    'FINANCE': get_sector_time_series_df('FINANCE'),
    'REAL ESTATE & CONSTRUCTION': get_sector_time_series_df('REAL ESTATE & CONSTRUCTION'),
    'MANUFACTURING': get_sector_time_series_df('MANUFACTURING'),
    'ENERGY & TRANSPORTATION': get_sector_time_series_df('ENERGY & TRANSPORTATION')
}

class ThreeMonthsPriceMovementPredictor:
    """
    This class is used to predict if the price of a
    given stock will go up or down. It also returns the
    factors(shap values) that lead to the model's prediction
    """
    _ml_model = joblib.load('/Users/orestis/MyProjects/InvestorAPI/analytics/machine_learning/price_prediction_with_fundamentals/ml_models/rf_three_months_prediction_model.joblib')
    _classifier = _ml_model.steps[1][1]
    _prediction_input_transformer = _ml_model.steps[0][1]
    _explainer = shap.TreeExplainer(_classifier)

    @classmethod
    def get_prediction_probabilities(cls, symbol: str) -> Dict[str, float]:
        """
        Returns a dictionary with the predicted probabilities for the 
        price of the symbol's stock. Example:
        {
            "up": 0.75,
            "down": 0.25
        }
        """
        prediction_input = cls._create_stock_prediction_input_data(symbol)
        prediction_probabilites = cls._ml_model.predict_proba(prediction_input)
        return {
            "down": prediction_probabilites[0][0],
            "up": prediction_probabilites[0][1]
        }

    @classmethod
    def get_prediction_factors(cls, symbol: str,  predicted_class: int):
        prediction_input = cls._create_stock_prediction_input_data(symbol)
        shap_values = cls._explainer.shap_values(cls._prediction_input_transformer.transform(prediction_input))
        features = cls._prediction_input_transformer.get_feature_names_out()
        features_with_shap_values = list()

        for i in range(len(features)):
            feature_name = features[i]
            shap_value = shap_values[predicted_class][0][i]
            features_with_shap_values.append((feature_name, shap_value))
        
        return sorted(features_with_shap_values, key=lambda x: x[1], reverse=True)

    @classmethod
    def _create_stock_prediction_input_data(cls, symbol: str) -> pd.DataFrame:
        stock_fundamental_df = get_stock_fundamental_df(symbol)
        stock_time_series_df = get_stock_time_series_df(symbol)

        stock_sector = stock_fundamental_df.iloc[0, stock_fundamental_df.columns.get_loc('sector')]
        sector_time_series_df = sectors_time_series.get(stock_sector)

        # Create stock prediction data
        current_date = dt.datetime.today()
        stock_prediction_data_df = pd.DataFrame([
            {"Date": current_date},
        ])
        stock_prediction_data_df['symbol'] = symbol
        stock_prediction_data_df['sector'] = stock_sector

        stock_prediction_data_df['interest_rate'] = stock_prediction_data_df['Date'].apply(
            find_time_series_most_recent_value,
            target_column='value',
            time_series_df=interest_rate_df,
            days=-93
        )

        stock_prediction_data_df['treasury_yield'] = stock_prediction_data_df['Date'].apply(
            find_time_series_most_recent_value,
            target_column='value',
            time_series_df=treasury_yield_df,
            days=-93
        )

        stock_prediction_data_df['price_pct_change_last_six_months'] = stock_prediction_data_df['Date'].apply(
            calculate_time_series_pct_change,
            target_column='close_price',
            time_series_df=stock_time_series_df,
            days=-186
        )

        stock_prediction_data_df['price_pct_change_last_three_months'] = stock_prediction_data_df['Date'].apply(
            calculate_time_series_pct_change,
            target_column='close_price',
            time_series_df=stock_time_series_df,
            days=-93
        )

        stock_prediction_data_df['price_pct_change_last_month'] = stock_prediction_data_df['Date'].apply(
            calculate_time_series_pct_change,
            target_column='close_price',
            time_series_df=stock_time_series_df,
            days=-33
        )

        stock_prediction_data_df['price_volatility_last_six_months'] = stock_prediction_data_df['Date'].apply(
            calculate_time_series_volatility,
            target_column='close_price',
            time_series_df=stock_time_series_df,
            days=-186
        )

        stock_prediction_data_df['price_volatility_last_three_months'] = stock_prediction_data_df['Date'].apply(
            calculate_time_series_volatility,
            target_column='close_price',
            time_series_df=stock_time_series_df,
            days=-93
        )

        stock_prediction_data_df['price_volatility_last_month'] = stock_prediction_data_df['Date'].apply(
            calculate_time_series_volatility,
            target_column='close_price',
            time_series_df=stock_time_series_df,
            days=-33
        )

        stock_prediction_data_df['sector_pct_change_last_six_months'] = stock_prediction_data_df['Date'].apply(
            calculate_sector_pct_change,
            time_series_df=sector_time_series_df,
            days=-186
        )

        stock_prediction_data_df['sector_pct_change_last_three_months'] = stock_prediction_data_df['Date'].apply(
            calculate_sector_pct_change,
            time_series_df=sector_time_series_df,
            days=-93
        )

        stock_prediction_data_df['sector_pct_change_last_month'] = stock_prediction_data_df['Date'].apply(
            calculate_sector_pct_change,
            time_series_df=sector_time_series_df,
            days=-33
        )

        financial_statements_columns = [col_name for col_name in stock_fundamental_df.columns if str(col_name).endswith('_arctan_pct_change')]
        stock_prediction_data_df[financial_statements_columns] = stock_prediction_data_df['Date'].apply(
            find_latest_financials_data,
            financials_time_series_df=stock_fundamental_df,
        )

        return stock_prediction_data_df#.drop(['symbol', 'Date'], axis=1, inplace=True)
