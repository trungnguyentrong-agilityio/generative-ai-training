import json
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from pydantic import BaseModel

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

class GoogleShoppingResult(BaseModel):
    products: list[ProductItem]

# class GoogleShoppingTool(BaseModel):
#     search_engine: SerpAPIWrapper
#     # TODO: extract product info from the search result
#     def extract_product_info(search_result: list[dict]) -> GoogleShoppingResult:

    # def _run(self, query: str) -> str:

# Function to use the tool
def create_google_shopping_tool() -> Tool:
    """
    Create a Google Shopping tool using SerpAPI.
    """

    params = {
        "engine": "google_shopping",
        "gl": "us",
        "hl": "en",
    }

    # search = SerpAPIWrapper(serpapi_api_key=settings.serpapi_api_key, params=params)
    
    return Tool(
        name="google_shopping_tool",
        # func=search.run,
        func=lambda x: load_json_from_file("/home/trungnguyen/workspaces/training/generative-ai-training/e_commerce_chatbot/data/google_shopping_data.json"),
        description="""A tool to search for product information using Google Shopping, 
        NOTE: this tool is only called when the user want to search for a product outside of the E-commerce platform.
        """
    )

if __name__ == "__main__":
    tool = create_google_shopping_tool()
    result = tool.run("iPhone 13")
    print(result)