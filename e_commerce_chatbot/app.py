import streamlit as st
from langchain.schema import ChatMessage


from e_commerce_chatbot.components.agent import create_e_commerce_agent
from e_commerce_chatbot.components.chat_memory import ConversationMemory


st.sidebar.title("Sample questions")
sample_questions = [
    "Hello, my name is Trung",
    "What is price of Iphone 13?",
    "What are supported payment methods?",
]
st.title("💬 E-commerce Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        ChatMessage(role="assistant", content="How can I help you?")
    ]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationMemory(
        k=6,
        return_messages=True,
        output_key="output",
        memory_key="chat_history"
    )

# Initialize agent
agent = create_e_commerce_agent(memory=st.session_state["memory"])

def process_input(prompt: str):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            response = agent.invoke({"input": prompt})["output"]
            st.session_state.messages.append(ChatMessage(role="assistant", content=response))
            message_placeholder.markdown(response)

for question in sample_questions:
    if st.sidebar.button(question):
        process_input(question)

if prompt := st.chat_input():
    process_input(prompt)
