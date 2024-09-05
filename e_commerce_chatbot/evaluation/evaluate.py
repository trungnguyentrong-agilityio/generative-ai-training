from e_commerce_chatbot import init_qa_chain


def call_api(prompt, options, context):
    qa_chain = init_qa_chain()
    response = qa_chain.invoke({"input": prompt})
    result = {
        "output": response,
    }

    return result
