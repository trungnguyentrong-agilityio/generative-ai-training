from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.tools import Tool
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool

from e_commerce_chatbot.config import settings

def create_faqs_tool() -> Tool:
    embedding_func = OpenAIEmbeddings(api_key=settings.openai_api_key, model=settings.openai_embedding_model)
    vector_db = Chroma(
        persist_directory=settings.chroma_persist_directory,
        embedding_function=embedding_func,
    )
    retriever = vector_db.as_retriever()
    tool = create_retriever_tool(
        retriever=retriever,
        name="retrieval_tool",
        description="A tool retrieves FAQs for E-commerce platform"
    )
    return tool

if __name__ == "__main__":
    tool = create_faqs_tool()
    print(tool.run("How do I track my order?"))
