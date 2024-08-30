import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma


# from components.model import chatbot_chain, messages
from components.chains.qa_chain import create_qa_chain
from components.rag_retriever import create_rag_retriever
from config import settings

# Initialize the QA chain and components
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


# Define chat UI
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key", key="chatbot_api_key", type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"

st.title("💬 E-commerce Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    stream = qa_chain.stream({"input": prompt})

    msg = st.chat_message("assistant").write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": msg})
