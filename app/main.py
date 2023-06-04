from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.graphql.api import schema
from app import dependencies
from app.api.routers import economic_indicators

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(economic_indicators.router)

@app.on_event("shutdown")
def shutdown_event():
    dependencies.close_db_conn()
