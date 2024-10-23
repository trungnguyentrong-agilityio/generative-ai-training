from typing import Optional
from sqlalchemy.engine import Engine
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.language_models import BaseChatModel
from langchain.tools import Tool
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from e_commerce_chatbot.config import settings


def create_sql_tool(db_engine: Engine, llm: Optional[BaseChatModel] = None) -> Tool:
    """
    Create a SQL agent as tool for the given database engine and language model.

    Args:
        db_engine: The database engine.
        llm: The language model.

    Returns:
        The SQLDatabaseToolkit.
    """
    
    db = SQLDatabase(db_engine)
    if llm is None:
        llm = ChatOpenAI(model=settings.openai_sql_llm_model, temperature=0, verbose=True)

    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    sql_agent = create_sql_agent(
        llm=llm,
        toolkit=sql_toolkit,
        verbose=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )

    return Tool(
        name="sql_tool",
        func=sql_agent.run,
        description="""A tool for querying product information, order processing, shipping information, return and refund information of the E-commerce platform. 
        This tool should be called as default when the user ask about the product information.
        """
    )
