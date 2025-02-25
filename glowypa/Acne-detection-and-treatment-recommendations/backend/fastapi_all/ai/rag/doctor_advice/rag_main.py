from db.chromaRag import ChromaStorage
from extract_data.document_convert import ExtractData
from extract_data.semantic_chunking import SemanticChunker
from typing import List, Dict, Any, Optional

class RagPipeline:
    """
    A pipeline class that combines document extraction, semantic chunking and vector storage.
    """
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.extractor = ExtractData()
        self.chunker = SemanticChunker(chunk_size=500,chunk_overlap=50)
        self.storage = None
        
    def extract_data(self, data_path: str) -> List[Dict[str, Any]]:
        return self.extractor.text_from_pdf(data_path)

    def semantic_chunk(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self.chunker.semantic_chunking_process(metadata)

    def chroma_storage_db(self, chunks: List[Dict[str, Any]]) -> ChromaStorage:
        self.storage = ChromaStorage(data=chunks)
        return self.storage.storage_db_vector()

    def search_engine(self, query: str, k: int = 5) -> List[Any]:
        if self.storage is None:
            raise ValueError("Vector store not initialized. Call chroma_storage_db first.")
        vectorstore = self.storage.storage_db_vector()
        return self.storage.query_top_k(
            vectorstore=vectorstore,
            query=query,
            k=k
        )


def main():
    metadata = []
    pipeline = RagPipeline(data_path="/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/doctor_advice/storage/Acne_Vulgaris.pdf")
    extracted_data = pipeline.extract_data(pipeline.data_path)
    metadata.append(extracted_data)
    chunks = pipeline.semantic_chunk(metadata)
    pipeline.chroma_storage_db(chunks)
    results = pipeline.search_engine("your search query")
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

if __name__ == "__main__":
    main()
