from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import create_db_conn
from app.api import schema
from app.api import serializers
from app.services.collections import CollectionsService

router = APIRouter(prefix='/collections')


@router.get(
    "/dividend_leaders",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.StockLeader]
)
async def get_dividend_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    dividend_leaders = service.get_dividend_leaders()
    return [
        serializers.serialize_stock_leader(dividend_leader)
        for dividend_leader in dividend_leaders
    ]


@router.get(
    "/reit_leaders",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.StockLeader]
)
async def get_reit_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    reit_leaders = service.get_reit_leaders()
    return [
        serializers.serialize_stock_leader(reit_leader)
        for reit_leader in reit_leaders
    ]


@router.get(
    "/utility_leaders",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.StockLeader]
)
async def get_utility_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    utility_leaders = service.get_utility_leaders()
    return [
        serializers.serialize_stock_leader(utility_leader)
        for utility_leader in utility_leaders
    ]


@router.get(
    "/tech_leaders",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.TechLeader]
)
async def get_tech_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    tech_leaders = service.get_tech_leaders()
    return [
        serializers.serialize_tech_leader(tech_leader)
        for tech_leader in tech_leaders
    ]


@router.get(
    "/top_200_overall_rated_stocks",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.Stock]
)
async def get_top_overall_rated_stocks_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    stocks = service.get_top_composite_stocks()
    return [
        serializers.serialize_stock(stock)
        for stock in stocks
    ]


@router.get(
    "/eps_rating_leaders",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.Stock]
)
async def get_eps_rating_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    stocks = service.get_eps_rating_leaders()
    return [
        serializers.serialize_stock(stock)
        for stock in stocks
    ]


@router.get(
    "/price_strength_rating_leaders",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.Stock]
)
async def get_rs_rating_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    stocks = service.get_price_rs_rating_leaders()
    return [
        serializers.serialize_stock(stock)
        for stock in stocks
    ]


@router.get(
    "/stocks_under_heavy_buying",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.Stock]
)
async def get_stocks_under_heavy_buying_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    stocks = service.get_stocks_under_heavy_buying()
    return [
        serializers.serialize_stock(stock)
        for stock in stocks
    ]


@router.get(
    "/stocks_under_heavy_selling",
    tags=["Collections"],
    status_code=200,
    response_model=List[schema.Stock]
)
async def get_stocks_under_heavy_selling_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    stocks = service.get_stocks_under_heavy_selling()
    return [
        serializers.serialize_stock(stock)
        for stock in stocks
    ]
