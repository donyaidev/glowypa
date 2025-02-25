from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np 
from typing import List
import uvicorn
import torch
from huggingface_hub import login
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import hf_hub_download


login(token="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")

torch.cuda.empty_cache()
# Initialize FastAPI app
app = FastAPI(title="Embedding API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả origins - trong production nên chỉ định cụ thể
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả methods (GET, POST, etc.)
    allow_headers=["*"],  # Cho phép tất cả headers
)
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Initialize the embedding model
model = SentenceTransformer('BAAI/bge-m3', cache_folder='./model_cache', device=device)

# Input model
class TextInput(BaseModel):
    text: str
    
class TextInputList(BaseModel):
    texts: List[str]  # Nhận một danh sách các chuỗi


# Output model
class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimension: int
class EmbeddingResponseList(BaseModel):
    embeddings: List[List[float]]  # Trả về danh sách các embeddings
    dimensions: int  # Kích thước của mỗi embedding
    
@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    global model
    print("Loading model...")

@app.post("/get_embedding", response_model=EmbeddingResponse)
async def get_embedding(input_data: TextInput):
    print(input_data)
    try:
        # Generate embedding
        embedding = model.encode([input_data.text])[0]
        embedding_list = embedding.tolist()
        return {
            "embedding": embedding_list,
            "dimension": len(embedding_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/get_embeddings")
async def get_embedding(input_data: TextInputList):
    print(input_data)
    try:
        embeddings = model.encode(input_data.texts)
        embedding_list = [embedding.tolist() for embedding in embeddings]
        return {
            "embeddings": embedding_list,
            "dimensions": len(embedding_list[0]) if embedding_list else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

