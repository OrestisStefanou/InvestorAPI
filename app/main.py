from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.graphql.api import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
