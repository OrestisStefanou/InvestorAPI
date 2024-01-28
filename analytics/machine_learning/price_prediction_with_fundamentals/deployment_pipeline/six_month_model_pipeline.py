from analytics.machine_learning.price_prediction_with_fundamentals.deployment_pipeline.base_model_pipeline import BaseModelPipeline

class SixMonthModelPipeline(BaseModelPipeline):
    def __init__(self) -> None:
        super().__init__(
            months=6,
            target_price_column='price_pct_change_next_six_months', 
            current_model_path='/Users/orestis/MyProjects/InvestorAPI/analytics/machine_learning/price_prediction_with_fundamentals/ml_models/rf_six_months_prediction_model.joblib',
            true_negative_threshold=0.85,
            true_positive_threshold=0.85
        )
