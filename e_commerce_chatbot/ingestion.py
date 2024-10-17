from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
import pandas as pd
from sqlalchemy import text

from config import settings
from components.document_loader import load_document
from db import get_db_engine

RETURN_AND_REFUND_PATH = "data/returns-and-refunds.csv"
SHIPPING_INFO_PATH = "data/shipping-info.txt"
ORDER_PROCESS_PATH = "data/order-process.json"
FAQS_PATH = "data/faqs.txt"
PRODUCT_INFORMATION_PATH = "/home/trungnguyen/workspaces/training/generative-ai-training/e_commerce_chatbot/data/products.csv"

def load_products(engine):
    """
    Load products into the database.

    Args:
        engine: The SQL database engine.
    """
    df = pd.read_csv(PRODUCT_INFORMATION_PATH)
    
    # Clean up column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    with engine.connect() as conn:
        # Get category and sub-category mappings
        category_map = pd.read_sql("SELECT id, name FROM categories", conn).set_index('name')['id'].to_dict()
        sub_category_map = pd.read_sql("SELECT id, name, category_id FROM sub_categories", conn)
        sub_category_map = sub_category_map.set_index(['name', 'category_id'])['id'].to_dict()

        # Insert products
        for _, row in df.iterrows():
            category_id = category_map.get(row['category'])
            if category_id is None:
                print(f"Warning: Category '{row['category']}' not found. Skipping product '{row['name']}'.")
                continue

            sub_category_id = sub_category_map.get((row['sub_category'], category_id))
            if sub_category_id is None:
                print(f"Warning: Sub-category '{row['sub_category']}' not found for category '{row['category']}'. Skipping product '{row['name']}'.")
                continue

            conn.execute(text("""
            INSERT INTO products (name, description, price, sub_category_id)
            VALUES (:name, :description, :price, :sub_category_id)
            """), {
                'name': row['name'],
                'description': row['description'],
                'price': float(row['price'].replace('$', '')),
                'sub_category_id': sub_category_id
            })

        conn.commit()

def load_faqs():
    """
    Embedding FAQs documents and save the vector database.
    """
    faqs_documents = load_document(FAQS_PATH)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=150)
    splitted_docs = text_splitter.split_documents(faqs_documents)
    embedding_func = OpenAIEmbeddings(api_key=settings.openai_api_key) # type: ignore
    Chroma.from_documents(
        documents=splitted_docs,
        embedding=embedding_func,
        persist_directory=settings.chroma_persist_directory,
    )

if __name__ == "__main__":
    # Create a connection to the database
    engine = get_db_engine(read_only=False)

    # Load products
    load_products(engine)

    # Load FAQs
    load_faqs()