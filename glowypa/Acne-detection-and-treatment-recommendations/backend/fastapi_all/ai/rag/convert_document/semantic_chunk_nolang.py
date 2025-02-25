import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List, Dict
import re
from tqdm import tqdm

class TextSplitter:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_text(self, text: str) -> List[Dict]:
        # Xóa khoảng trắng thừa và chuẩn hóa
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split theo câu dựa trên dấu câu của cả tiếng Việt và tiếng Nhật
        pattern = r'([.!?。．！？]+[\s\n]*)'
        sentences = re.split(pattern, text)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = []
        current_length = 0
        start_idx = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length <= self.chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_length
            else:
                if current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    chunks.append({
                        'text': chunk_text,
                        'start_idx': start_idx,
                        'end_idx': start_idx + len(chunk_text),
                        'sentences': current_chunk.copy()
                    })
                    
                    # Xử lý overlap
                    overlap_sentences = current_chunk[-1:] if self.chunk_overlap > 0 else []
                    current_chunk = overlap_sentences + [sentence]
                    current_length = sum(len(s) for s in current_chunk)
                    start_idx = start_idx + len(chunk_text) - len(overlap_sentences[0]) if overlap_sentences else start_idx + len(chunk_text)
                else:
                    # Nếu một câu dài hơn chunk_size, chia nhỏ nó
                    sub_chunks = [sentence[i:i + self.chunk_size] for i in range(0, len(sentence), self.chunk_size)]
                    for sub_chunk in sub_chunks:
                        chunks.append({
                            'text': sub_chunk,
                            'start_idx': start_idx,
                            'end_idx': start_idx + len(sub_chunk),
                            'sentences': [sub_chunk]
                        })
                        start_idx += len(sub_chunk)
                    current_chunk = []
                    current_length = 0
        
        # Xử lý chunk cuối cùng
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                'text': chunk_text,
                'start_idx': start_idx,
                'end_idx': start_idx + len(chunk_text),
                'sentences': current_chunk
            })
        
        return chunks

class TextEmbedding:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", batch_size: int = 32):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        self.batch_size = batch_size
        
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        embeddings = []
        
        # Xử lý theo batch để tránh tràn bộ nhớ
        for i in tqdm(range(0, len(texts), self.batch_size), desc="Creating embeddings"):
            batch_texts = texts[i:i + self.batch_size]
            
            # Tokenize
            encoded_input = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt'
            ).to(self.device)
            
            # Compute token embeddings
            with torch.no_grad():
                model_output = self.model(**encoded_input)
            
            # Perform pooling
            batch_embeddings = self.mean_pooling(model_output, encoded_input['attention_mask'])
            
            # Convert to numpy and store
            batch_embeddings = batch_embeddings.cpu().numpy()
            embeddings.extend(batch_embeddings)
            
        return np.array(embeddings)

# Ví dụ sử dụng:
def process_document(text: str, chunk_size: int = 500, chunk_overlap: int = 50):
    # Khởi tạo
    splitter = TextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embedder = TextEmbedding()
    
    # Split text
    chunks = splitter.split_text(text)
    
    # Tạo embeddings
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embedder.get_embeddings(texts)
    
    # Thêm embeddings vào chunks
    for i, chunk in enumerate(chunks):
        chunk['embedding'] = embeddings[i]
    
    return chunks

# Sử dụng
if __name__ == "__main__":
    # Ví dụ văn bản đa ngôn ngữ
    text = """
    これは日本語のテキストです。とても長い文章です。
    複数の段落があります。
    
    Đây là một đoạn văn bản tiếng Việt.
    Nó có nhiều câu và nhiều đoạn.
    Chúng ta đang thử nghiệm việc tách văn bản.
    """
    
    results = process_document(text, chunk_size=200, chunk_overlap=20)
    
    # In kết quả
    for i, chunk in enumerate(results):
        print(f"\nChunk {i+1}:")
        print(f"Text: {chunk['text']}")
        print(f"Start index: {chunk['start_idx']}")
        print(f"End index: {chunk['end_idx']}")
        print(f"Number of sentences: {len(chunk['sentences'])}")
        print(f"Embedding shape: {chunk['embedding'].shape}")
