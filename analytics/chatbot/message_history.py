from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri(f"sqlite:///sqlite.db")

chat_message_history = SQLChatMessageHistory(
    session_id="test_session_id", connection=db._engine
)

print(chat_message_history)