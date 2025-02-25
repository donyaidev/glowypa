from langdetect import detect, detect_langs, LangDetectException
import os
from typing import List
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity
import re
import logging
import requests
logger = logging.getLogger(__name__)
import string

def embedding_calling(input_data: list):
    url_call = "http://0.0.0.0:8888/get_embeddings"  
    try:
        response = requests.post(url_call, json={"texts": input_data})
        if response.status_code == 200:
            embedding_texts = response.json()['embeddings']
            return np.array(embedding_texts)  
        else:
            logging.error(f"API Error: {response.status_code}, {response.text}")
            return None
    except BaseException as e:
        logging.error(f"Error: {e}")
        return None
    
def embeddding_calling(input_data: str):
    url_call = "http://0.0.0.0:8888/get_embedding"
    try:
        response = requests.post(url_call, json={"text": input_data})
        if response.status_code == 200:
            embeddding_text = response.json()['embedding']
            return np.array(embeddding_text)
    except BaseException as e:
        logging.error(f"Error: {e}")
        
class TextChunkingError(Exception):
    """Custom exception cho quá trình chia chunk"""
    pass

class SemanticChunker:
    def __init__(self, 
                 chunk_size: int = 512, 
                 chunk_overlap: int = 50, 
                 language: str = None):
        """
        Khởi tạo Semantic Chunker
        Args:
            chunk_size: Kích thước tối đa của mỗi chunk
            chunk_overlap: Độ chồng lấp giữa các chunk
            embedding_model: Model embedding sử dụng
            language: Ngôn ngữ xử lý ('vi', 'ja', 'en'). Nếu None sẽ tự động detect
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.language = language
        self.separators = None
        self.lang = None
    def detect_language(self, text: str) -> str:
        """
        Tự động nhận diện ngôn ngữ của văn bản sử dụng 
        """
        text = ' '.join(text.split())
        lang_code = detect(text)
        lang_map = {
            'vi': 'vietnamese',
            'ja': 'japanese',
            'en': 'english'
        }
        logger.debug(lang_code)
        self.lang = lang_code
        return lang_map.get(lang_code)
 

    def _get_language_separators(self, language: str) -> List[str]:
        """
        Trả về danh sách các separator phù hợp với từng ngôn ngữ
        """
        common_separators = ["\n\n", "\n", ". ", ", ", " "]
        if language == "japanese":
            return ["。", "、", "！", "？", "」", "』", "）", "\n\n", "\n", " "] + common_separators
        elif language == "vietnamese":
            return [". ", "; ", ", ", ": ", "? ", "! ", "\n\n", "\n", " "] + common_separators
        else:  # english and others
            return common_separators

    def clean_text(self, text: str, language: str) -> str:
        """
        Làm sạch văn bản theo đặc thù của từng ngôn ngữ
        """
        text = text.strip()
        if language == "japanese":
            text = re.sub(r'[\s\u3000]+', ' ', text)
            text = re.sub(r'([。、！？」』）])\s*', r'\1\n', text)
        elif language == "vietnamese":
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\s*([\.,!?;:])\s*', r'\1 ', text)
            text = re.sub(r'\(\s+', '(', text)
            text = re.sub(r'\s+\)', ')', text)
        return text

    # def split_text(self, text: str) -> List[str]:
    #     """
    #     Chia văn bản thành các chunk
    #     """
    #     self.language = self.detect_language(text)
    #     self.separators = self._get_language_separators(self.language)
    #     self.text_splitter = RecursiveCharacterTextSplitter(
    #         chunk_size=self.chunk_size,
    #         chunk_overlap=self.chunk_overlap,
    #         length_function=len,
    #         separators=self.separators,
    #         is_separator_regex=False
    #     )
    #     text = self.clean_text(text, self.language)
    #     chunks = self.text_splitter.split_text(text)
    #     processed_chunks = []
    #     for chunk in chunks:
    #         chunk = chunk.strip()
    #         if not chunk:
    #             continue
    #         if self.language == "japanese":
    #             if not chunk[-1] in ["。", "！", "？", "」", "』", "）"]:
    #                 chunk += "。"
    #         elif self.language == "vietnamese":
    #             if not chunk[-1] in [".", "!", "?", "..."]:
    #                 chunk += "."
    #         processed_chunks.append(chunk)
    #     return processed_chunks
    def detect_language(self, text: str) -> str:
        """
        Phát hiện ngôn ngữ của văn bản.
        
        Args:
            text (str): Văn bản cần phát hiện ngôn ngữ
            
        Returns:
            str: Mã ngôn ngữ (mặc định 'vi' nếu không phát hiện được)
        """
        if not text or not isinstance(text, str):
            logging.warning("Văn bản trống hoặc không phải chuỗi, sử dụng mặc định 'vi'")
            return 'vi'
            
        # Làm sạch và chuẩn bị văn bản
        text = text.strip()
        if len(text) < 10:  # Văn bản quá ngắn
            logging.warning("Văn bản quá ngắn để phát hiện ngôn ngữ, sử dụng mặc định 'vi'")
            return 'vi'
            
        try:
            # Thử phát hiện ngôn ngữ
            lang_code = detect(text)
            logging.info(f"Đã phát hiện ngôn ngữ: {lang_code}")
            return lang_code
        except LangDetectException as e:
            logging.warning(f"Không thể phát hiện ngôn ngữ: {str(e)}, sử dụng mặc định 'vi'")
            return 'vi'
        except Exception as e:
            logging.error(f"Lỗi không mong đợi khi phát hiện ngôn ngữ: {str(e)}")
            return 'vi'

    def split_text(self, text: str) -> List[str]:
        """
        Chia văn bản thành các chunk
        """
        try:
            # Kiểm tra và làm sạch văn bản đầu vào
            if not text or not isinstance(text, str):
                logging.warning("Văn bản đầu vào không hợp lệ")
                return []
                
            text = text.strip()
            if not text:
                logging.warning("Văn bản sau khi làm sạch trống")
                return []

            # Phát hiện ngôn ngữ và thiết lập các thông số
            self.language = self.detect_language(text)
            self.separators = self._get_language_separators(self.language)
            
            # Khởi tạo text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
                separators=self.separators,
                is_separator_regex=False
            )

            # Làm sạch và chia văn bản
            cleaned_text = self.clean_text(text, self.language)
            if not cleaned_text:
                return []
                
            chunks = self.text_splitter.split_text(cleaned_text)
            processed_chunks = []

            # Xử lý từng chunk
            for chunk in chunks:
                chunk = chunk.strip()
                if not chunk:
                    continue
                    
                # Thêm dấu câu cuối nếu cần
                if self.language == "japanese":
                    end_marks = ["。", "！", "？", "」", "』", "）"]
                    if not any(chunk.endswith(mark) for mark in end_marks):
                        chunk += "。"
                elif self.language in ["vietnamese", "vi"]:
                    end_marks = [".", "!", "?", "..."]
                    if not any(chunk.endswith(mark) for mark in end_marks):
                        chunk += "."
                        
                processed_chunks.append(chunk)

            return processed_chunks

        except Exception as e:
            logging.error(f"Lỗi trong quá trình chia văn bản: {str(e)}")
            return []  # Trả về list rỗng thay vì raise exception


    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Tạo embeddings cho danh sách các đoạn văn bản
        """
        # embeddings = self.embedding_model.embed_documents(texts)
        embeddings = embedding_calling(texts)

        return np.array(embeddings)

    def get_similarity_matrix(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Tính ma trận similarity giữa các embeddings
        """
        return cosine_similarity(embeddings)

    def merge_similar_chunks(self, chunks: List[str], similarity_threshold: float = 0.8) -> List[str]:
        """
        Gộp các chunk có độ tương đồng cao
        """
        if len(chunks) <= 1:
            return chunks
        embeddings = self.get_embeddings(chunks)
        similarity_matrix = self.get_similarity_matrix(embeddings)
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
                separator = " " if self.language != "japanese" else ""
                merged_chunk = separator.join([current_chunk] + to_merge)
                if len(merged_chunk) <= self.chunk_size * 2:
                    merged_chunks.append(merged_chunk)
                else:
                    merged_chunks.append(current_chunk)
                    for chunk in to_merge:
                        merged_chunks.append(chunk)
            else:
                merged_chunks.append(current_chunk)
        return merged_chunks
    
    def process_text(self, text: str, similarity_threshold: float = 0.8) -> List[str]:
        """
        Xử lý văn bản đầu vào: tách chunk và gộp các chunk tương tự
        """
        chunks = self.split_text(text)
        merged_chunks = self.merge_similar_chunks(chunks, similarity_threshold)
        return merged_chunks    
    
    def clean_text_chunk(self, text):
        """
        Hàm làm sạch văn bản với các bước:
        1. Chuyển về chữ thường
        2. Loại bỏ dấu câu 
        3. Loại bỏ khoảng trắng thừa
        4. Loại bỏ ký tự đặc biệt (giữ lại số)
        
        Args:
            text (str): Văn bản cần làm sạch
            
        Returns:
            str: Văn bản đã được làm sạch
        """
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'[^\w\s\d]', '', text)
        text = ' '.join(text.split())
        return text
    
    def semantic_chunking_process(self, metadata: list[object]) -> list[object]:
        metadata_chunked = []
        
        for document in metadata:
            for page in document['pages']:
                result = self.process_text(document['pages'][f'{page}'])
                for index, chunk in enumerate(result):
                    metadata_chunked.append({
                        "file_name": document['file_name'],
                        "page": page.split("_", 1)[1],
                        "text": self.clean_text_chunk(chunk),
                        "embedding": embeddding_calling(input_data=self.clean_text_chunk(chunk)).tolist()
                    })
                    print(self.clean_text_chunk(chunk))
                    print('-'*100)
        return metadata_chunked
