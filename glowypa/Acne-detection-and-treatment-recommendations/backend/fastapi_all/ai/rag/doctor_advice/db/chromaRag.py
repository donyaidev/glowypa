import logging
from typing import List, Dict, Any, Optional
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings

class ChromaStorage:
    """
    A class to handle document storage and retrieval using Chroma vector store.
    """
    def __init__(
        self, 
        data: List[Dict[str, Any]] = [], 
        embedding_model: str = "BAAI/bge-m3"
    ) -> None:
        """
        Initialize ChromaStorage with documents and embedding model.

        Args:
            data: List of dictionaries containing document data
            embedding_model: Name of the HuggingFace embedding model to use
        """
        self.document = self._convert_data(data)
        self.embedding_model = HuggingFaceEmbeddings(model_name=embedding_model)

    def _convert_data(self, data: List[Dict[str, Any]]) -> List[Document]:
        """
        Convert raw data into Langchain Document objects.

        Args:
            data: List of dictionaries containing document data with format:
                [{"filename": str, "text": str}, ...]

        Returns:
            List of Document objects
        """
        documents = []
        for item in data:
            doc = Document(
                page_content=item["text"],
                metadata={
                    "filename": item["file_name"]
                }
            )
            documents.append(doc)
        return documents

    def storage_db_vector(self) -> Chroma:
        """
        Create and return a Chroma vector store from the documents.

        Returns:
            Chroma vector store instance
        """
        return Chroma.from_documents(
            documents=self.document, 
            embedding=self.embedding_model
        )

    def query_top_k(
        self, 
        vectorstore: Chroma, 
        query: str,
        k: int = 5, 
        fetch_k: int = 5, 
        lambda_mult: float = 0.7
    ) -> List[Document]:
        """
        Query the vector store for similar documents.

        Args:
            vectorstore: Chroma vector store instance
            query: Search query string
            k: Number of results to return
            fetch_k: Number of documents to fetch for MMR
            lambda_mult: MMR diversity parameter

        Returns:
            List of relevant Document objects
        """
        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": fetch_k,
                "lambda_mult": lambda_mult
            }
        )
        return retriever.get_relevant_documents(query)
