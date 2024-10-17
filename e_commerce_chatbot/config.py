from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    openai_api_key: str = Field(default=...)
    openai_llm_model: str = Field(default="gpt-3.5-turbo")
    openai_embedding_model: str = Field(default="text-embedding-ada-002")

    langchain_api_key: str = Field(default=...)

    chroma_persist_directory: str = Field(default="chroma_db")

    serpapi_api_key: str = Field(default=...)

    postgres_db: str = Field(default="e_commerce_db")
    postgres_user: str = Field(default=...)
    postgres_password: str = Field(default=...)
    postgres_port: int = Field(default=5432)
    postgres_host: str = Field(default="localhost")
    postgres_read_only_user: str = Field(default="read_only_user")
    postgres_read_only_password: str = Field(default="read_only_password")

settings = Settings()
