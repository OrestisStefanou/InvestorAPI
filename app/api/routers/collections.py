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
    response_model=List[schema.DividendLeader]
)
async def get_dividend_leaders_collection(
    db_session = Depends(create_db_conn)
):
    service = CollectionsService(db_session)
    dividend_leaders = service.get_dividend_leaders()
    return [
        serializers.serialize_dividend_leaders(dividend_leader)
        for dividend_leader in dividend_leaders
    ]