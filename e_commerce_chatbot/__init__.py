from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma


from e_commerce_chatbot.components.chains.qa_chain import create_qa_chain
from e_commerce_chatbot.components.rag_retriever import create_rag_retriever
from e_commerce_chatbot.config import settings


def init_qa_chain():
    """
    Initialize the QA chain and components
    """

    embedding_func = OpenAIEmbeddings(api_key=settings.openai_api_key)
    chat_model = ChatOpenAI(
        api_key=settings.openai_api_key, model=settings.openai_llm_model
    )
    vector_db = Chroma(
        persist_directory=settings.chroma_persist_directory,
        embedding_function=embedding_func,
    )
    rag_retriever = create_rag_retriever(vector_store=vector_db)
    qa_chain = create_qa_chain(chat_model, rag_retriever)

    return qa_chain
