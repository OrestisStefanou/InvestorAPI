from http import HTTPStatus

from fastapi import (
    APIRouter,
    HTTPException
)

from app.api import serializers
from app.api import schema
from analytics.chatbot.agent import InvestorAgent
from analytics.chatbot.prompt import examples

router = APIRouter()

@router.post(
    "/chatbot/conversation",
    tags=["Chatbot"],
    status_code=200,
    response_model=list[schema.ConversationMessage]
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
    response_model=list[str]
)
async def get_question_examples():
    return [
        example['input'] for example in examples
    ]