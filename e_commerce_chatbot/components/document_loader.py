import os
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_community.document_loaders import (
    TextLoader,
    JSONLoader,
    CSVLoader,
)
from pathlib import Path

class DocumentLoaderInvalidFormat(Exception):
    pass

class DocumentFileNotFound(Exception):
    pass

def load_document(path: str | Path, **loaderKargs) -> list[Document]:
    """
    Load data file into standard LangChain Document format

    Args:
        path: Path to file to load.

    Returns: list of standard LangChain Document
    """

    if isinstance(path, str):
        path = Path(path)

    if not os.path.isfile(path):
        raise DocumentFileNotFound(f"{path.name} not found!")

    suffix = path.suffix
    loader_cls: type[BaseLoader]

    match suffix:
        case ".txt":
            loader_cls = TextLoader

        case ".csv":
            loader_cls = CSVLoader

        case ".json":
            loader_cls = JSONLoader

        case _:
            raise DocumentLoaderInvalidFormat(f"{suffix} is not supported!")


    loader = loader_cls(file_path=path, **loaderKargs)
    return loader.load()
