import datetime as dt
from typing import Dict, List, Set, Any, Optional

import pandas as pd
import shap
from sklearn.pipeline import Pipeline

from analytics.utils import (
    get_stock_time_series_df,
    get_stock_symbols
)
from analytics.machine_learning.price_prediction_with_fundamentals.utils import (
    get_stock_fundamental_df,
    add_timeseries_features,
    get_sector_time_series
)
from analytics.errors import (
    PredictionDataNotFound,
    InvalidPredictionInput
)

features_map = {
    'onehotencoder__sector_ENERGY & TRANSPORTATION': 'Stock Sector',
    'onehotencoder__sector_FINANCE': 'Stock Sector',
    'onehotencoder__sector_LIFE SCIENCES': 'Stock Sector',
    'onehotencoder__sector_MANUFACTURING': 'Stock Sector',
    'onehotencoder__sector_REAL ESTATE & CONSTRUCTION': 'Stock Sector',
    'onehotencoder__sector_TECHNOLOGY': 'Stock Sector',
    'onehotencoder__sector_TRADE & SERVICES': 'Stock Sector',
    'remainder__interest_rate': 'Interest Rates', 
    'remainder__treasury_yield': 'Treasury Yield',
    'remainder__price_pct_change_last_six_months': 'Stock returns last 6 months',
    'remainder__price_pct_change_last_three_months': 'Stock returns last 3 months',
    'remainder__price_pct_change_last_month': 'Stock returns last 1 month',
    'remainder__price_volatility_last_six_months': 'Stock price volatility last 6 months',
    'remainder__price_volatility_last_three_months': 'Stock price volatility last 3 months',
    'remainder__price_volatility_last_month': 'Stock price volatility last 1 month',
    'remainder__sector_pct_change_last_six_months': 'Stock Sector performance last 6 months',
    'remainder__sector_pct_change_last_three_months': 'Stock Sector performance last 3 months',
    'remainder__sector_pct_change_last_month': 'Stock Sector performance last 1 month',
    'remainder__capital_expenditures_arctan_pct_change': 'Capital expenditure change quarter over quarter',
    'remainder__cash_and_cash_equivalents_at_carrying_value_arctan_pct_change': 'Cash and Cash Equivalents change quarter over quarter',
    'remainder__cashflow_from_financing_arctan_pct_change': 'Cashflow from financing change quarter over quarter',
    'remainder__cashflow_from_investment_arctan_pct_change': 'Cashflow from investment change quarter over quarter',
    'remainder__current_net_receivables_arctan_pct_change': 'Current net receivables change quarter over quarter',
    'remainder__dividend_payout_arctan_pct_change': 'Dividend payout change quarter over quarter',
    'remainder__ebitda_arctan_pct_change': 'EBITDA change quarter over quarter',
    'remainder__gross_profit_arctan_pct_change': 'Gross profit change quarter over quarter',
    'remainder__inventory_arctan_pct_change': 'Inventory change quarter over quarter',
    'remainder__long_term_debt_arctan_pct_change': 'Long term debt change quarter over quarter',
    'remainder__net_income_arctan_pct_change': 'Net income change quaerter over quarter',
    'remainder__net_interest_income_arctan_pct_change': 'Net interest income change quaerter over quarter',
    'remainder__operating_cashflow_arctan_pct_change': 'Operating cashflow change quarter over quarter',
    'remainder__operating_income_arctan_pct_change': 'Operating income change quarter over quarter',
    'remainder__payments_for_repurchase_of_equity_arctan_pct_change': 'Payments for repurchase of equity change quarter over quarter',
    'remainder__proceeds_from_issuance_of_long_term_debt_and_capital_securities_net_arctan_pct_change': 'Net proceeds from long-term debt and capital securities issuance change quarter over quarter',
    'remainder__property_plant_equipment_arctan_pct_change': 'Property plant equipment change quarter over quarter',
    'remainder__total_assets_arctan_pct_change': 'Total assets change quarter over quarter',
    'remainder__total_current_assets_arctan_pct_change': 'Total current assets change quarter over quarter',
    'remainder__total_current_liabilities_arctan_pct_change': 'Total current liabilities change quarter over quarter',
    'remainder__total_liabilities_arctan_pct_change': 'Total liabilities change quarter over quarter',
    'remainder__total_revenue_arctan_pct_change': 'Total revenue change quarter over quarter',
    'remainder__total_shareholder_equity_arctan_pct_change': 'Total shareholder equity change quarter over quarter',
    'remainder__current_debt_arctan_pct_change': 'Current debt change quarter over quarter',
    'remainder__cost_of_goods_and_services_sold_arctan_pct_change': 'Cost of services sold change quarter over quarter',
    'remainder__current_debt_arctan_pct_change': 'Current debt change quarter over quarter',
    'remainder__common_stock_shares_outstanding_arctan_pct_change': 'Common stock shares outstanding change quarter over quarter',
    'remainder__eps': 'Earnings per share',
    'remainder__revenue_per_share': 'Revenue per share',
    'remainder__book_value_per_share': 'Book value per share',
    'remainder__gross_profit_margin': 'Gross profit margin',
    'remainder__operating_profit_margin': 'Operating profit margin',
    'remainder__return_on_assets': 'Return on assets',
    'remainder__return_on_equity': 'Return on equity',
    'remainder__cash_to_debt_ratio': 'Cash to debt ratio',
    'remainder__assets_to_liabilities_ratio': 'Assets to liabilities ratio',
    'remainder__pe_ratio': 'Price to earnings ratio',
    'remainder__price_to_book_ratio': 'Price to book ratio',
    'remainder__price_to_sales_ratio': 'Price to sales ratio',
}

class PriceMovementPredictor:
    """
    This class is used to predict if the price of a
    given stock will go up or down. It also returns the
    factors(shap values) that lead to the model's prediction.
    This should be used as a base class, any class that inherits
    from this one should override the _ml_model class variable which
    is a Pipeline object with two steps:
        1. Column transformer
        2. Classifier
    """
    _ml_model: Pipeline = None

    @classmethod
    def get_prediction_probabilities_with_prediction_factors(cls, symbol: str) -> Dict[str, Any]:
        """
        Returns a dictionary with the predicted probabilities for the 
        price of the symbol's stock. Example:
        {
            "prediction_probabilities": {
                "up": 0.75,
                "down": 0.25
            },
            "prediction_factors": {
                "up": ['Stock Sector', 'Net interest income change quaerter over quarter',],
                "down": ['Interest Rates', 'Total liabilities change quarter over quarter']
            }
        }
        """
        prediction_input = cls._create_stock_prediction_input_data(symbol)
        cls._validate_prediction_input(prediction_input)
        prediction_probabilites = cls._ml_model.predict_proba(prediction_input)
        down_prediction_factors = cls._get_prediction_factors(prediction_input, 0)
        up_prediction_factors = cls._get_prediction_factors(prediction_input, 1)
        return {
            'prediction_probabilities':{
                'down': prediction_probabilites[0][0],
                'up': prediction_probabilites[0][1]
            },
            'prediction_factors': {
                'down': list(down_prediction_factors),
                'up': list(up_prediction_factors)
            }
        }

    @classmethod
    def _get_prediction_factors(cls, prediction_input: pd.DataFrame, predicted_class: int) -> Set[str]:
        classifier = cls._ml_model.steps[1][1]
        explainer = shap.TreeExplainer(classifier)
        prediction_input_transformer = cls._ml_model.steps[0][1]
        cls._validate_prediction_input(prediction_input)
        shap_values = explainer.shap_values(prediction_input_transformer.transform(prediction_input))
        features = prediction_input_transformer.get_feature_names_out()
        features_with_shap_values = list()

        for i in range(len(features)):
            feature_name = features[i]
            shap_value = shap_values[predicted_class][0][i]
            if shap_value > 0:
                features_with_shap_values.append((feature_name, shap_value))
        
        return {
            features_map[x[0]] 
            for x in sorted(features_with_shap_values, key=lambda x: x[1], reverse=True)
        }

    @classmethod
    def get_high_probabilities_predictions(cls, threshold:float = 0.70) -> List[Dict[str, Any]]:
        """
        Returns the predictions with probability above the given threshold.
        Example response
        [
            {
                'symbol': 'NVDA',
                'prediction_probability': 0.75,
                'prediction': 'up'
            },
        ]
        """
        high_probabilities_predictions = list()
        labels_map = {
            0: 'down',
            1: 'up'
        }
        # 1. Get all the stock symbols we have
        symbols = get_stock_symbols()
        # 2. Create the prediction input
        for symbol in symbols:
            prediction_input = cls._create_stock_prediction_input_data(symbol)
            try:
                cls._validate_prediction_input(prediction_input)
            except Exception:
                continue

            predicted_label = cls._ml_model.predict(prediction_input)[0]
            prediction_probabilities = cls._ml_model.predict_proba(prediction_input)[0]
            if prediction_probabilities[predicted_label] >= threshold:
                high_probabilities_predictions.append({
                    'symbol': symbol,
                    'prediction_probability': prediction_probabilities[predicted_label],
                    'prediction': labels_map[predicted_label]
                })

        return high_probabilities_predictions

    @classmethod
    def _validate_prediction_input(cls, prediction_input: pd.DataFrame) -> None:
        if prediction_input is None:
            raise PredictionDataNotFound('Prediction data not available')

        nan_columns = prediction_input.columns[prediction_input.isna().any()].tolist()
        if len(nan_columns) > 0:
            raise InvalidPredictionInput(f"Features with NaN values: {nan_columns}")

    @classmethod
    def _create_stock_prediction_input_data(cls, symbol: str) -> Optional[pd.DataFrame]:
        stock_fundamental_df = get_stock_fundamental_df(symbol)
        if stock_fundamental_df.empty:
            return None

        stock_time_series_df = get_stock_time_series_df(symbol)

        stock_sector = stock_fundamental_df.iloc[0, stock_fundamental_df.columns.get_loc('sector')]
        sector_time_series_df = get_sector_time_series(stock_sector)

        if sector_time_series_df is None:
            return None
        
        # Create stock prediction data
        current_date = dt.datetime.today()
        stock_prediction_data_df = pd.DataFrame([
            {"Date": current_date},
        ])
        stock_prediction_data_df['symbol'] = symbol
        stock_prediction_data_df['sector'] = stock_sector

        return add_timeseries_features(
            stock_prediction_data_df=stock_prediction_data_df,
            stock_fundamental_df=stock_fundamental_df,
            stock_time_series_df=stock_time_series_df,
            sector_time_series_df=sector_time_series_df
        )
