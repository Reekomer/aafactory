import pandas as pd
from functools import lru_cache
from enum import Enum
from pydantic import BaseModel
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document
from langchain.retrievers import TFIDFRetriever
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

GERMAN_STOP_WORDS = list(stopwords.words('german'))


class RetrieverEnum(str, Enum):
    EmbeddingMethod = "HuggingFaceEmbeddings"
    TFIDFRetrieverMethod = "TFIDFRetriever"


class RetrieverMethod(BaseModel):
    retriever: RetrieverEnum


def retrieve_relevant_documents(prompt: str, retriever_method: RetrieverMethod, history: list=[]) -> list[Document]:
    if retriever_method.retriever == RetrieverEnum.EmbeddingMethod:
        retriever = load_embedding_db()
        return retriever.similarity_search(prompt)
    elif retriever_method.retriever == RetrieverEnum.TFIDFRetrieverMethod:
        retriever = load_sparse_vector_db()
        return retriever.get_relevant_documents(prompt)


@lru_cache(maxsize=None)
def load_embedding_db() -> FAISS:
    """Load the sparse vector database"""
    article_documents = _process_article_csv_for_embedding()
    text_splitter = CharacterTextSplitter(separator = "\n", chunk_size=1000, chunk_overlap=0, length_function=len)
    documents = text_splitter.split_documents(article_documents)
    model_name = "danielheinz/e5-base-sts-en-de"
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': False}
    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db


def _process_article_csv_for_embedding() -> list[Document]:
    docs = []
    articles_df = pd.read_csv(os.getenv("DOCUMENTATION_CSV_PATH"))
    articles_df["file_content"] = articles_df["file_content"].str.wrap(100).str.strip()
    articles_df.fillna('', inplace=True)
    for _, row in articles_df.iterrows():
        docs.append(Document(
            page_content=row["file_content"],
            metadata={"file_name": row["file_name"], "category": row["category"], "url": row["url"]}
        ))
    return docs


@lru_cache(maxsize=None)
def load_sparse_vector_db() -> TFIDFRetriever:
    """Load the sparse vector database"""
    article_documents = _process_article_csv_for_embedding()
    text_splitter = CharacterTextSplitter(separator = "\n", chunk_size=500, chunk_overlap=0, length_function=len)
    documents = text_splitter.split_documents(article_documents)
    return TFIDFRetriever.from_documents(k=2, documents=documents, analyzer='word' , tfidf_params={'stop_words':GERMAN_STOP_WORDS} )
