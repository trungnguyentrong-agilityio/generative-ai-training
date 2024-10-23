from typing import Optional, Sequence
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.callbacks import Callbacks
from langchain_core.prompts import PromptTemplate
from langchain_core.memory import BaseMemory

from e_commerce_chatbot.components.prompts import E_COMMERCE_PROMPT
from e_commerce_chatbot.components.tools import create_google_shopping_tool, create_sql_tool, create_faqs_tool
from e_commerce_chatbot.config import settings
from langchain_core.tools import BaseTool
from e_commerce_chatbot.db import get_db_engine

def create_e_commerce_agent(memory: Optional[BaseMemory] = None):
    # Initialize the language model
    llm = ChatOpenAI(model=settings.openai_llm_model, temperature=0.3, verbose=True)
    read_only_engine = get_db_engine(read_only=True)


    tools: Sequence[BaseTool] = [
        create_sql_tool(db_engine=read_only_engine),
        create_google_shopping_tool(),
        create_faqs_tool()
    ]

    react_prompt = PromptTemplate.from_template(E_COMMERCE_PROMPT)
    react_agent = create_react_agent(llm, tools, prompt=react_prompt)
    agent_executor = AgentExecutor(
        agent=react_agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        return_intermediate_steps=True,
        memory=memory
    )

    return agent_executor

if __name__ == "__main__":
    agent = create_e_commerce_agent()
    print(agent.get_prompts())
    result = agent.invoke({"input": "Hello, my name is Trung?"})
    print("Result: ", result)
