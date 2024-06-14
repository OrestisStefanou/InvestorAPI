from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.utilities import SQLDatabase

from app import settings

chatbot_db = SQLDatabase.from_uri(f"sqlite:///{settings.chatbot_db_path}")

chat_message_history = SQLChatMessageHistory(
    session_id="test_session_id_2", connection=chatbot_db._engine
)