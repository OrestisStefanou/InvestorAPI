from fastapi import APIRouter, Depends

from app.dependencies import create_db_conn
from app.domain.economic_indicator import EconomicIndicator
from app.api import schema
from app.api import serializers
from app.services.time_series import TimeSeriesService

router = APIRouter()


@router.get(
    "/economic_indicators/{indicator}/time_series",
    tags=["Economic Indicators"],
    status_code=200,
    response_model=schema.EconomicIndicatorTimeSeries
)
async def get_economic_indicator_time_series(
    indicator: schema.EconomicIndicator,
    db_session = Depends(create_db_conn)
):
    service = TimeSeriesService(db_session)
    time_series = service.get_economic_indicator_time_series(
        indicator=EconomicIndicator(indicator.value)
    )

    return schema.EconomicIndicatorTimeSeries(
        indicator=indicator,
        unit=time_series[0].unit,
        time_series=[
            serializers.serialize_economic_indicator_time_series_entry(
                time_series_entry
            )
            for time_series_entry in time_series
        ]
    )
