from e_commerce_chatbot import settings
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool


# Function to use the tool
def create_google_shopping_tool() -> Tool:
    params = {
        "engine": "google_shopping",
        "gl": "us",
        "hl": "en",
    }

    search = SerpAPIWrapper(serpapi_api_key=settings.serpapi_api_key, params=params)
    
    return Tool(
        name="Google Shopping Search",
        func=search.run,
        description="""A tool to search for product information and prices using Google Shopping, 
        input should be a product name or description. For example: 'iPhone 13',
        NOTE: this tool is only called when the user want to search for a product outside of the platform.
        """,
    )

if __name__ == "__main__":
    tool = create_google_shopping_tool()
    result = tool.run("iPhone 13")
    print(result)