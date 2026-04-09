from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS

from app.core.llm import llm
from app.core.loader import load_document
from app.core.embedding import embeddings
from app.core.vector_store import splitter

vectorstore = None
ragchain = None


def build_rag(file_path: str):
    global vectorstore, ragchain

    documents = load_document(file_path)
    print("Documents loaded:", len(documents))

    chunks = splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No chunks created")

    vectorstore = FAISS.from_documents(chunks, embeddings)

    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_template(
        """Answer the question using the context below.

        Context:
        {context}

        Question:
        {question}
        """
    )

    ragchain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
