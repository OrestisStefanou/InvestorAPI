from analytics.machine_learning.price_prediction_with_fundamentals.deployment_pipeline.base_model_pipeline import BaseModelPipeline

class ThreeMonthModelPipeline(BaseModelPipeline):
    def __init__(self) -> None:
        super().__init__(
            months=3,
            target_price_column='price_pct_change_next_three_months', 
            current_model_path='/Users/orestis/MyProjects/InvestorAPI/analytics/machine_learning/price_prediction_with_fundamentals/ml_models/rf_three_months_prediction_model.joblib'
        )
