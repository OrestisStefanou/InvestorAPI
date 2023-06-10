from http import HTTPStatus

from fastapi import (
    APIRouter,
    Depends,
    Path,
    HTTPException
)

from app.dependencies import create_db_conn
from app.api import schema
from app.api import serializers
from app.services.stocks_service import StocksService


router = APIRouter()


@router.get(
    "/stocks/{symbol}/profile",
    tags=["Stocks"],
    status_code=200,
    response_model=schema.Stock
)
async def get_stock_profile(
    symbol: str = Path(
        title="The symbol of the stock to get",
        min_length=1,
        max_length=6,
        regex='^[A-Z]+$'
    ),
    db_session = Depends(create_db_conn)
):
    service = StocksService(db_session)
    stock_profile = service.get_stock_profile(symbol)

    if stock_profile is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Stock with symbol {symbol} not found"
        )

    return serializers.serialize_stock(stock_profile)


@router.get(
    "/stocks/{symbol}/historical_performance",
    tags=["Stocks"],
    status_code=200,
    response_model=schema.StockHistoricalPerformance
)
async def get_stock_historical_performance(
    symbol: str = Path(
        title="The symbol of the stock to get",
        min_length=1,
        max_length=6,
        regex='^[A-Z]+$'
    ),
    db_session = Depends(create_db_conn)
):
    service = StocksService(db_session)
    stock_performance_data = service.get_stock_historical_performance(symbol)

    if len(stock_performance_data) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Stock with symbol {symbol} not found"
        )

    return serializers.serialize_stock_historical_performance(stock_performance_data)