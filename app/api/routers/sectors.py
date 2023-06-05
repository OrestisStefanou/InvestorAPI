from typing import List

from fastapi import APIRouter, Depends

from app.domain.sector import Sector
from app.dependencies import create_db_conn
from app.api import schema
from app.api import serializers
from app.services.sectors import SectorService

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
    service = SectorService(db_session)
    stocks = service.get_sector_stocks(Sector(sector.value))
    return [
        serializers.serialize_stock(stock)
        for stock in stocks
    ]
