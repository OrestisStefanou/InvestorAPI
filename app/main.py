from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.graphql.api import schema
from app import dependencies
from app.api.routers import (
    economic_indicators,
    world_indices,
    collections,
    sectors,
    stocks,
    machine_learning
)

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(economic_indicators.router)
app.include_router(world_indices.router)
app.include_router(collections.router)
app.include_router(sectors.router)
app.include_router(stocks.router)
app.include_router(machine_learning.router)


@app.on_event("shutdown")
def shutdown_event():
    dependencies.close_db_conn()
