from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.graphql.api import schema
from app import dependencies

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

@app.on_event("shutdown")
def shutdown_event():
    dependencies.db_conn.close()