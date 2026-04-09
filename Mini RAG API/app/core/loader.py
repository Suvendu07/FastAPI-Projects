from langchain_community.document_loaders import PyPDFLoader, TextLoader
import os

def load_document(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()  

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        return loader.load()

    elif ext == ".txt":
        loader = PyPDFLoader(file_path, encoding = "utf-8")
        return loader.load()

    else:
        raise ValueError(f"Unsupported file type: {ext}")
