from typing import List, Optional
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

class SemanticChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        embedding_model: str = "BAAI/bge-m3"
    ):
        """
        Khởi tạo Semantic Chunker
        
        Args:
            chunk_size: Kích thước tối đa của mỗi chunk
            chunk_overlap: Độ chồng lấp giữa các chunk
            embedding_model: Model embedding sử dụng
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=embedding_model
        )

    def split_text(self, text: str) -> List[str]:
        """
        Chia văn bản thành các chunk
        
        Args:
            text: Văn bản đầu vào
            
        Returns:
            List các chunk văn bản
        """
        return self.text_splitter.split_text(text)

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Tạo embedding vectors cho list các văn bản
        
        Args:
            texts: List các văn bản
            
        Returns:
            Ma trận embedding vectors
        """
        embeddings = self.embedding_model.embed_documents(texts)
        return np.array(embeddings)

    def get_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Tính ma trận similarity giữa các embedding vectors
        
        Args:
            embeddings: Ma trận embedding vectors
            
        Returns:
            Ma trận similarity
        """
        return cosine_similarity(embeddings)

    def merge_similar_chunks(
        self,
        chunks: List[str],
        similarity_threshold: float = 0.8
    ) -> List[str]:
        """
        Gộp các chunk có độ tương đồng cao
        
        Args:
            chunks: List các chunk văn bản
            similarity_threshold: Ngưỡng similarity để gộp chunks
            
        Returns:
            List các chunk sau khi gộp
        """
        if len(chunks) <= 1:
            return chunks

        # Tạo embeddings
        embeddings = self.get_embeddings(chunks)
        
        # Tính similarity matrix
        similarity_matrix = self.get_similarity_matrix(embeddings)

        # Gộp chunks
        merged_chunks = []
        skip_indices = set()

        for i in range(len(chunks)):
            if i in skip_indices:
                continue

            current_chunk = chunks[i]
            to_merge = []

            for j in range(i + 1, len(chunks)):
                if j in skip_indices:
                    continue
                    
                if similarity_matrix[i][j] >= similarity_threshold:
                    to_merge.append(chunks[j])
                    skip_indices.add(j)

            if to_merge:
                merged_chunk = " ".join([current_chunk] + to_merge)
                merged_chunks.append(merged_chunk)
            else:
                merged_chunks.append(current_chunk)

        return merged_chunks

    def process_text(
        self,
        text: str,
        similarity_threshold: float = 0.8
    ) -> List[str]:
        """
        Xử lý văn bản: chia thành chunks và gộp các chunk tương tự
        
        Args:
            text: Văn bản đầu vào
            similarity_threshold: Ngưỡng similarity để gộp chunks
            
        Returns:
            List các chunk sau khi xử lý
        """
        # Chia văn bản thành chunks
        chunks = self.split_text(text)
        
        # Gộp các chunk tương tự
        merged_chunks = self.merge_similar_chunks(
            chunks,
            similarity_threshold
        )
        return merged_chunks

# Ví dụ sử dụng
if __name__ == "__main__":
    # Khởi tạo chunker
    chunker = SemanticChunker(
        chunk_size=300,
        chunk_overlap=30
    )
    
    # Văn bản mẫu
    text = """
 私の日常生活について話したいと思います。毎朝6時に目覚まし時計が鳴ります。ベッドから起き上がって、まずシャワーを浴びます。その後、簡単な朝食を作って食べます。普段は食パンとスクランブルエッグ、それにホットコーヒーです。

    8時までに家を出て、電車で会社に向かいます。通勤時間は約45分です。電車の中では主にスマートフォンでニュースを読んだり、音楽を聴いたりしています。時々、電子書籍も読みます。

    会社では主にコンピューターを使って仕事をします。午前中は集中力が高いので、重要な仕事を済ませるようにしています。昼休みは同僚とオフィス近くのレストランで食事をすることが多いです。午後は会議が多く、顧客との電話やメールのやり取りもあります。

    仕事が終わった後は、週に3回ほどジムに通っています。健康維持のために、1時間程度の運動をします。帰宅後は簡単な夕食を作って、テレビを見たり、本を読んだりしてリラックスします。

    休日は友達と出かけたり、部屋の掃除をしたり、趣味の料理を楽しんだりします。時には近くの公園を散歩することもあります。
    """
    
    # Xử lý văn bản
    chunks = chunker.process_text(
        text,
        similarity_threshold=0.8
    )
    
    # In kết quả
    print("Processed chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i}:")
        print(chunk)
