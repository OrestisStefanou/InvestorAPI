from typing import List

from fastapi import APIRouter, Depends

from app.domain.sector import Sector
from app.dependencies import create_db_conn
from app.api import schema
from app.api import serializers
from app.services.sectors import SectorService

router = APIRouter()


def _sector_schema_to_domain_model(sector_schema: schema.Sector) -> Sector:
    """
    We use this function because the values of schema.Sector.FOOD_BEV
    and schema.Sector.ALCOHL_TOB don't match the values of the domain Sector
    values. The reason they don't match is because having / in the enum causes
    problems in the endpoint
    """
    if sector_schema == schema.Sector.FOOD_BEV:
        return Sector.FOOD_BEV
    
    if sector_schema == schema.Sector.ALCOHL_TOB:
        return Sector.ALCOHL_TOB
    
    return Sector(sector_schema.value)


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
    stocks = service.get_sector_stocks(
        sector=_sector_schema_to_domain_model(sector)
    )
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


@router.get(
    "/sectors/{sector}/performance",
    tags=["Sectors"],
    status_code=200,
    response_model=List[schema.SectorPerformanceEntry]
)
async def get_sectors_performance(
    sector: schema.Sector,
    db_session = Depends(create_db_conn)
):
    service = SectorService(db_session)
    sector_historical_performance = service.get_sector_performance(
        sector=_sector_schema_to_domain_model(sector)
    )
    
    response = []
    for date, sector_performance in sector_historical_performance.items():
        response.append(
            schema.SectorPerformanceEntry(
                date=date,
                sector_performance=serializers.serialize_sector_performance(sector_performance)
            )
        )

    return response
