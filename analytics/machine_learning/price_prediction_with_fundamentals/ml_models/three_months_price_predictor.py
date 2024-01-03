import joblib

from analytics.machine_learning.price_prediction_with_fundamentals.ml_models.base_predictor import PriceMovementPredictor


class ThreeMonthsPriceMovementPredictor(PriceMovementPredictor):
    _ml_model = joblib.load('/Users/orestis/MyProjects/InvestorAPI/analytics/machine_learning/price_prediction_with_fundamentals/ml_models/rf_three_months_prediction_model.joblib')
