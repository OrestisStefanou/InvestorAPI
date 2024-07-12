from typing import List
from http import HTTPStatus

from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)

from app.api import serializers
from app.api import schema
from analytics.chatbot.agent import InvestorAgent
from analytics.chatbot.prompt import examples
from app.dependencies import create_db_conn
from app.repos.sql_repo import SqlRepo

router = APIRouter()

@router.post(
    "/chatbot/conversation",
    tags=["Chatbot"],
    status_code=200,
    response_model=List[schema.ConversationMessage]
)
async def create_conversation(question: schema.ChatbotQuestion):
    agent = InvestorAgent()
    try:
        conversation = agent.chat(
            question=question.question,
            session_id=question.session_id
        )
    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )

    return [
        serializers.serialize_chatbot_conversation_message(message)
        for message in conversation
    ]


@router.get(
    "/chatbot/question_examples",
    tags=["Chatbot"],
    status_code=200,
    response_model=schema.ChatbotQuestionExamples
)
async def get_question_examples():
    return schema.ChatbotQuestionExamples(
        examples=[
            example['input'] for example in examples
    ])


@router.get(
    "/chatbot/context",
    tags=["Chatbot"],
    status_code=200,
    response_model=List[schema.ChatbotDatabaseContext]
)
async def get_chatbot_context(db_session = Depends(create_db_conn)):
    db_repo = SqlRepo(db_session)
    db_context = db_repo.get_database_context()

    return [
        schema.ChatbotDatabaseContext(
            table_name=context['table_name'],
            table_columns=context['table_columns'],
        )
        for context in db_context
    ]