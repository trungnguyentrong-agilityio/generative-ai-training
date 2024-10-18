from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain import hub

from e_commerce_chatbot.components.tools.google_shopping_tool import create_google_shopping_tool
from e_commerce_chatbot.components.tools.sql_tool import create_sql_tool
from e_commerce_chatbot.db import get_db_engine

def create_e_commerce_agent():
    # Initialize the language model
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5, verbose=True)
    read_only_engine = get_db_engine(read_only=True)


    tools: list[Tool] = [
        create_google_shopping_tool(),
        create_sql_tool(read_only_engine, llm)
    ]

    react_prompt = hub.pull("hwchase17/react")
    react_agent = create_react_agent(llm, tools, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True)

    return agent_executor

if __name__ == "__main__":
    agent = create_e_commerce_agent()
    agent.invoke({"input": "What is the price of an iPhone 13 on google shopping and compare it with the price on your platform?"})
