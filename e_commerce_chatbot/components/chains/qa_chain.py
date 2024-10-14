from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from operator import itemgetter
from typing import Literal
from typing_extensions import TypedDict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.router.multi_prompt_prompt import MULTI_PROMPT_ROUTER_TEMPLATE

system_qa_prompt_template = """You are a excellent E-commerce ChatBot assistant \
Your role is to help customers by providing accurate, concise and friendly responses \
about ordering process, shipping, returns and refunds, and common customer issues/solutions \
to their inquirers based on the provided information delimited by triple backticks. \
If you encounter a query out of scope or don't know the answer, politely suggest the customer contact live support or visit the help center.
IMPORTANT: don't make up a story for the answer!!!

Provided information:
```
{context}
```
"""

system_production_prompt_template = """You are a excellent E-commerce ChatBot assistant \
Your role is to help customers by providing accurate, concise and friendly responses \
about product information to their inquirers based on the provided production list delimited by triple backticks. \
If you encounter a query for non-existent product, politely suggest the customer contact live support or visit the help center.
IMPORTANT: don't make up a story for queried product!!!

Provided production list:
```
{context}
```

Example output:
```
Name: Apple iPhone 13 Pro \n
Description: The iPhone 13 Pro is a powerful smartphone with a 6.1-inch Super Retina XDR display, A15 Bionic chip, and advanced camera system. Available in Sierra Blue, Silver, Gold, and Graphite colors. \n
Price: $999
```
"""

human_prompt_template = "{input}"

prompt_infos = [
    {
        "name": "production information",
        "description": "Good for answering questions about product information",
    },
    {
        "name": "Q&A",
        "description": "Good for answering questions about ordering process, shipping, returns, and common customer issues/solutions",
    },
]


# Define schema for router chain output:
class RouteQuery(TypedDict):
    """Route query to destination expert."""

    destination: Literal["production information", "Q&A"]


def create_router_chain(chat_model: BaseChatModel):
    destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
    router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations)
    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", router_template),
            ("human", "{input}"),
        ]
    )

    return (
        route_prompt
        | chat_model.with_structured_output(RouteQuery)
        | itemgetter("destination")
    )


def create_product_chain(
    chat_model: BaseChatModel,
    retriever: VectorStoreRetriever,
    system_prompt: str,
):
    chatbot_system_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["context"], template=system_prompt)
    )
    chatbot_human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["input"], template=human_prompt_template)
    )
    messages = [chatbot_system_prompt, chatbot_human_prompt]
    chatbot_prompt_template = ChatPromptTemplate(
        input_variables=["context", "input"], messages=messages
    )

    chain = (
        {
            "context": RunnableLambda(lambda x: x["input"]) | retriever | format_doc,
            "input": lambda x: x["input"],
        }
        | chatbot_prompt_template
        | chat_model
        | StrOutputParser()
    )

    return chain


def create_question_answer_chain(
    chat_model: BaseChatModel, retriever: VectorStoreRetriever, system_prompt: str
):
    chatbot_system_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["context"], template=system_prompt)
    )
    chatbot_human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["input"], template=human_prompt_template)
    )
    messages = [chatbot_system_prompt, chatbot_human_prompt]
    chatbot_prompt_template = ChatPromptTemplate(
        input_variables=["context", "input"], messages=messages
    )

    chain = (
        {
            "context": RunnableLambda(lambda x: x["input"]) | retriever | format_doc,
            "input": lambda x: x["input"],
        }
        | chatbot_prompt_template
        | chat_model
        | StrOutputParser()
    )

    return chain


def format_doc(docs: list[Document]) -> str:
    return "\n".join([doc.page_content for doc in docs])


def create_qa_chain(
    chat_model: BaseChatModel,
    retriever: VectorStoreRetriever,
    product_system_prompt: str = system_production_prompt_template,
    qa_system_prompt: str = system_qa_prompt_template,
):
    product_chain = create_product_chain(
        chat_model=chat_model, retriever=retriever, system_prompt=product_system_prompt
    )
    qa_chain = create_question_answer_chain(
        chat_model=chat_model, retriever=retriever, system_prompt=qa_system_prompt
    )

    route_chain = create_router_chain(chat_model=chat_model)

    chain = {
        "destination": route_chain,
        "input": lambda x: x["input"],
    } | RunnableLambda(
        lambda x: qa_chain if x["destination"] == "Q&A" else product_chain
    )

    return chain
