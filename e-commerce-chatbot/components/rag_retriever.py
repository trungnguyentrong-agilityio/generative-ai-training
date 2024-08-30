from langchain_core.vectorstores import VectorStore
from langchain_core.vectorstores import VectorStoreRetriever


def create_rag_retriever(vector_store: VectorStore) -> VectorStoreRetriever:
    return vector_store.as_retriever()
