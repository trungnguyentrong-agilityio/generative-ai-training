from sqlalchemy.engine import Engine
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.language_models import BaseChatModel
from langchain.tools import Tool
from langchain_community.agent_toolkits.sql.base import create_sql_agent

from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


def create_sql_tool(db_engine: Engine, llm: BaseChatModel) -> Tool:
    """
    Create a SQL agent as tool for the given database engine and language model.

    Args:
        db_engine: The database engine.
        llm: The language model.

    Returns:
        The SQLDatabaseToolkit.
    """
    
    db = SQLDatabase(db_engine)
    sql_toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    sql_agent = create_sql_agent(llm=llm, toolkit=sql_toolkit, verbose=True)

    return Tool(
            name="SQL Database Search",
            func=sql_agent.run,
            description="""A tool for product information, order processing, shipping information, return and refund information. 
            This tool should be called as default when the user ask about the product information""",
        )
