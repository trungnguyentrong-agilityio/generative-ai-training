import json
from typing import Any
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from pydantic import BaseModel
from langchain_core.tools import BaseTool

from e_commerce_chatbot import settings

def load_json_from_file(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return json.load(file)

class ProductItem(BaseModel):
    title: str
    product_link: str
    source: str
    price: str
    thumbnail: str

def extract_product_info(search_result: list[dict]) -> list[dict]:
    products: list[dict] = []
    for item in search_result:
        product = ProductItem(
            title=item.get("title", ''),
            product_link=item.get("product_link", ''),
            source=item.get("source", ''),
            price=item.get("price", ''),
            thumbnail=item.get("thumbnail", '')
        )
        products.append(product.model_dump())
    
    return products


# Function to use the tool
def create_google_shopping_tool() -> BaseTool:
    """
    Create a Google Shopping tool using SerpAPI.
    """

    params = {
        "engine": "google_shopping",
        "gl": "us",
        "hl": "en",
    }

    search = SerpAPIWrapper(serpapi_api_key=settings.serpapi_api_key, params=params)

    def search_and_extract(query: str) -> list[dict[str, Any]]:
        # raw_results = search.run(query)
        raw_results = load_json_from_file("/home/trungnguyen/workspaces/training/generative-ai-training/e_commerce_chatbot/data/google_shopping_data.json")
        extracted_results = extract_product_info(raw_results) # type: ignore
        return extracted_results
    
    return Tool(
        name="google_shopping_tool",
        func=search_and_extract,
        description="""A tool to search for product information using Google Shopping, 
        NOTE: this tool is only called when the user want to search for a product outside of the E-commerce platform.
        """
    )

if __name__ == "__main__":
    tool = create_google_shopping_tool()
    result = tool.run("iPhone 13")
    print(result)
