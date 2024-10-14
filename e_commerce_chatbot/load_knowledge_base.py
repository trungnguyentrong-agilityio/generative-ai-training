from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings

from config import settings
from components.document_loader import load_document

RETURN_AND_REFUND_PATH = "data/returns-and-refunds.csv"
SHIPPING_INFO_PATH = "data/shipping-info.txt"
ORDER_PROCESS_PATH = "data/order-process.json"
FAQS_PATH = "data/faqs.txt"
PRODUCT_INFORMATION_PATH = "data/products-information.csv"

faqs_documents = load_document(FAQS_PATH)
order_process_documents = load_document(
    ORDER_PROCESS_PATH, jq_schema="{steps, payment_methods}", text_content=False
)
return_and_refunds_documents = load_document(RETURN_AND_REFUND_PATH)
shipping_info_documents = load_document(SHIPPING_INFO_PATH)
product_information_documents = load_document(PRODUCT_INFORMATION_PATH)

documents: list[Document] = (
    faqs_documents
    + order_process_documents
    + return_and_refunds_documents
    + shipping_info_documents
    + product_information_documents
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=150)
splitted_docs = text_splitter.split_documents(documents)

embedding_func = OpenAIEmbeddings(api_key=settings.openai_api_key)

Chroma.from_documents(
    documents=splitted_docs,
    embedding=embedding_func,
    persist_directory=settings.chroma_persist_directory,
)
