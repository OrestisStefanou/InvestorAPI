from fastapi import APIRouter

from analytics.machine_learning.price_prediction_with_fundamentals.ml_models.three_months_price_predictor import ThreeMonthsPriceMovementPredictor
from app.api import schema

router = APIRouter(prefix='/price_predictions')

@router.get(
    "/fundamentals_models/three_months_prediction",
    tags=["Machine Learning"],
    status_code=200,
    response_model=schema.FundamentalsPricePrediction
)
async def get_three_months_price_prediction_with_fundamentals(symbol: str):
    predictions_with_factors = ThreeMonthsPriceMovementPredictor.get_prediction_probabilities_with_prediction_factors(
        symbol=symbol
    )
    
    # Add some error handling

    # Serialize the response
    return ThreeMonthsPriceMovementPredictor.get_prediction_probabilities_with_prediction_factors(
        symbol=symbol
    )
