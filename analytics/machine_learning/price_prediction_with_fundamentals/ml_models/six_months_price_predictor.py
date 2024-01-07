import joblib

from analytics.machine_learning.price_prediction_with_fundamentals.ml_models.base_predictor import PriceMovementPredictor


class SixMonthsPriceMovementPredictor(PriceMovementPredictor):
    _ml_model = joblib.load('analytics/machine_learning/price_prediction_with_fundamentals/ml_models/rf_six_months_prediction_model.joblib')
