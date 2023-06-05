from typing import List

from fastapi import APIRouter, Depends

from app.dependencies import create_db_conn
from app.api import schema
from app.api import serializers

router = APIRouter()


@router.get(
    "/sectors/{sector}/stocks",
    tags=["Sectors"],
    status_code=200,
    response_model=List[schema.Stock]
)
async def get_sector_stocks(
    sector: schema.Sector,
    db_session = Depends(create_db_conn)
):
    pass
