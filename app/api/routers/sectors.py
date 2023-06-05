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


@router.get(
    "/sectors/performance",
    tags=["Sectors"],
    status_code=200,
    response_model=List[schema.SectorsPerformanceEntry]
)
async def get_sectors_performance(
    db_session = Depends(create_db_conn)
):
    service = SectorService(db_session)
    sectors_historical_performance = service.get_sectors_performance()
    
    response = []
    for date, sectors_performance in sectors_historical_performance.items():
        response.append(
            schema.SectorsPerformanceEntry(
                date=date,
                sectors_performance=[
                    serializers.serialize_sector_performance(performance)
                    for performance in sectors_performance
                ]
            )
        )

    return response
