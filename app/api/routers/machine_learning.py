
from fastapi import (
    APIRouter,
    HTTPException
)
from http import HTTPStatus

from analytics.machine_learning.price_prediction_with_fundamentals.ml_models.three_months_price_predictor import ThreeMonthsPriceMovementPredictor
from analytics.machine_learning.price_prediction_with_fundamentals.ml_models.six_months_price_predictor import SixMonthsPriceMovementPredictor
from analytics.errors import (
    PredictionDataNotFound,
    InvalidPredictionInput
)
from app.api import schema

router = APIRouter(prefix='/price_predictions')

@router.get(
    "/fundamentals_models/three_months_prediction",
    tags=["Machine Learning"],
    status_code=200,
    response_model=schema.FundamentalsPricePrediction
)
async def get_three_months_price_prediction_with_fundamentals(symbol: str):
    try:
        predictions_with_factors = ThreeMonthsPriceMovementPredictor.get_prediction_probabilities_with_prediction_factors(
            symbol=symbol
        )
    except PredictionDataNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Invalid or unsupported symbol'
        )
    except InvalidPredictionInput:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Something went wrong, we are working on it.'
        )

    # Serialize the response
    return schema.FundamentalsPricePrediction(
        prediction_probabilites=schema.PredictionProbabilities(
            up=predictions_with_factors['prediction_probabilities']['up'],
            down=predictions_with_factors['prediction_probabilities']['down']
        ),
        prediction_factors=schema.PredictionFactors(
            up=predictions_with_factors['prediction_factors']['up'],
            down=predictions_with_factors['prediction_factors']['down'],
        )
    )


@router.get(
    "/fundamentals_models/six_months_prediction",
    tags=["Machine Learning"],
    status_code=200,
    response_model=schema.FundamentalsPricePrediction
)
async def get_six_months_price_prediction_with_fundamentals(symbol: str):
    try:
        predictions_with_factors = SixMonthsPriceMovementPredictor.get_prediction_probabilities_with_prediction_factors(
            symbol=symbol
        )
    except PredictionDataNotFound:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Invalid or unsupported symbol'
        )
    except InvalidPredictionInput:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Something went wrong, we are working on it.'
        )

    # Serialize the response
    return schema.FundamentalsPricePrediction(
        prediction_probabilites=schema.PredictionProbabilities(
            up=predictions_with_factors['prediction_probabilities']['up'],
            down=predictions_with_factors['prediction_probabilities']['down']
        ),
        prediction_factors=schema.PredictionFactors(
            up=predictions_with_factors['prediction_factors']['up'],
            down=predictions_with_factors['prediction_factors']['down'],
        )
    )