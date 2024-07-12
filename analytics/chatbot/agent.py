from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages.base import BaseMessage

from app import settings
from analytics.chatbot.prompt import (
    full_prompt,
    context
)

class InvestorAgent:
    def __init__(
        self,
        temperature: float = 0.4,
        model: str = "gpt-3.5-turbo-0125"
    ) -> None:
        self._llm = ChatOpenAI(
            model=model,
            temperature=temperature, 
            openai_api_key=settings.openai_key
        )
        self._stock_db = SQLDatabase.from_uri(f"sqlite:///{settings.db_path}")
        self._sql_agent = create_sql_agent(
            llm=self._llm,
            toolkit=SQLDatabaseToolkit(db=self._stock_db, llm=self._llm),
            prompt=full_prompt,
            verbose=True,
            agent_executor_kwargs={"handle_parsing_errors":True},
            agent_type="tool-calling",
            max_iterations=10,
        )
        self._conversation_db = SQLDatabase.from_uri(f"sqlite:///{settings.chatbot_db_path}")
    
    def chat(self, question: str, session_id: str) -> list[BaseMessage]:
        chat_message_history = SQLChatMessageHistory(
            session_id=session_id, 
            connection=self._conversation_db._engine
        )

        chat_message_history.add_user_message(question)
        response = self._sql_agent.invoke(
            {
                "input": question,
                "top_k": 5,
                "dialect": "SQLite",
                "context": context,
                "agent_scratchpad": [],
                "messages": chat_message_history.messages,
            }
        )
        output = response["output"]
        chat_message_history.add_ai_message(output)
        return chat_message_history.messages
