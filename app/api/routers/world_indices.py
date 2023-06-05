from fastapi import APIRouter, Depends

from app.dependencies import create_db_conn
from app.domain.world_index import WorldIndex
from app.api import schema
from app.api import serializers
from app.services.time_series import TimeSeriesService

router = APIRouter()


@router.get(
    "/world_indices/{index}/time_series",
    tags=["World Indices"],
    status_code=200,
    response_model=schema.IndexTimeSeries
)
async def get_index_time_series(
    index: schema.WorldIndex,
    db_session = Depends(create_db_conn)
):
    service = TimeSeriesService(db_session)
    time_series = service.get_index_time_series(
        index=WorldIndex(index.value)
    )

    return schema.IndexTimeSeries(
        index=index,
        time_series=[
            serializers.serialize_index_time_series_entry(
                time_series_entry
            )
            for time_series_entry in time_series
        ]
    )
