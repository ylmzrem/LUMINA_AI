from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from typing import List


def create_vector_store(documents: List[Document], api_key: str) -> FAISS:
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )
    return FAISS.from_documents(documents, embeddings)


def get_retriever(vector_store: FAISS, k: int = 5):
    return vector_store.as_retriever(search_kwargs={"k": k})
