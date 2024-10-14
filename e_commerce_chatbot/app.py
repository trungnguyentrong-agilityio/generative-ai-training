import streamlit as st
from e_commerce_chatbot import init_qa_chain

# Initialize qa chain
qa_chain = init_qa_chain()


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
