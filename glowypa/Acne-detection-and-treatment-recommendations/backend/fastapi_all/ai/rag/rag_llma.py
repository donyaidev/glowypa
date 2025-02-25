# Import các thư viện cần thiết
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from ai.rag.doctor_advice.db.chromaRag import ChromaStorage
from ai.rag.doctor_advice.extract_data.document_convert import ExtractData
from ai.rag.doctor_advice.extract_data.semantic_chunking import SemanticChunker
from typing import List, Dict, Any, Optional
import os
import ollama
import markdown
import time
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from openai import OpenAI

token = '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'
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
client = OpenAI(
base_url=endpoint,
api_key=token,
)


# Định nghĩa system prompt như một constant
SYSTEM_PROMPT_TEMPLATE = """Bạn là trợ lý chuyên gia điều trị mụn của Glowypa:

1. THÔNG TIN VAI TRÒ:
- Bạn là bác sĩ tư vấn trực tiếp của Glowypa, chuyên về điều trị và tư vấn mụn
- Khi được hỏi, xác nhận bạn là trợ lý AI của Glowypa
- Sử dụng giọng điệu chuyên nghiệp, thân thiện và đồng cảm

2. NGUYÊN TẮC TƯ VẤN:
- Nếu chưa có thông tin về loại mụn, hướng dẫn người dùng sử dụng Acne Scan Daily và Medical Record của Glowypa
- Khuyên đi khám bác sĩ khi tình trạng mụn thực sự nghiêm trọng
- Đưa ra lời khuyên dựa trên bằng chứng và kiến thức chuyên môn
- Trả lời bằng tiếng Việt, rõ ràng và dễ hiểu
- Không sử dụng từ ngữ không phù hợp

# THÔNG TIN BỆNH NHÂN:
{medical_db}

KIẾN THỨC THAM KHẢO:
{chunk_text}

# LỊCH SỬ TƯ VẤN:
{chatHistoryCache}

Vui lòng trả lời theo dạng Markdown 

sau nếu người dùng hỏi về phân tích, phương pháp điều trị mụn và người dùng có mụn mới dùng formt bên dưới:
## 👨‍⚕️ Phân tích tình trạng
- Dựa trên thông tin bệnh nhân cung cấp
- Đánh giá mức độ và loại mụn
- Các yếu tố liên quan

## 💊 Giải pháp điều trị
### Những việc cần làm ngay
- Bước 1: [Hành động cụ thể]
- Bước 2: [Hành động cụ thể]
...

### Sản phẩm khuyên dùng
- Sản phẩm 1: [Tên và công dụng]
- Sản phẩm 2: [Tên và công dụng]
...

## ⚠️ Lưu ý quan trọng
- Điều cần tránh
- Cảnh báo (nếu có)
- Thời gian điều trị dự kiến

## 📋 Lời khuyên bổ sung
- Chế độ ăn uống
- Lifestyle
- Các tips hữu ích

## 🔄 Theo dõi và đánh giá
- Cách theo dõi tiến triển
- Khi nào cần tái khám
- Dấu hiệu cải thiện cần chú ý
"""

class RagPipeline:
    """
    A pipeline class that combines document extraction, semantic chunking and vector storage.
    """
    def __init__(self, data_path: str) -> None:
        """
        Initialize the RAG pipeline
        
        Args:
            data_path (str): Path to the data directory
        """
        self.data_path = data_path
        self.extractor = ExtractData()
        self.chunker = SemanticChunker(chunk_size=512, chunk_overlap=50)
        self.storage = None

    def extract_path(self, data_path: str) -> List[str]:
        """
        Extract file paths from the data directory
        
        Args:
            data_path (str): Path to the data directory
            
        Returns:
            List[str]: List of file paths
        """
        files = os.listdir(data_path)
        return [os.path.join(data_path, file) for file in files]

    def extract_data(self) -> List[Dict[str, Any]]:
        """
        Extract data from all files in the data directory
        
        Returns:
            List[Dict[str, Any]]: List of extracted metadata
        """
        return [self.extractor.text_from_pdf(path) for path in self.extract_path(self.data_path)]

    def semantic_chunk(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process semantic chunking on the metadata
        
        Args:
            metadata (List[Dict[str, Any]]): List of metadata to chunk
            
        Returns:
            List[Dict[str, Any]]: Processed chunks
        """
        return self.chunker.semantic_chunking_process(metadata)

    def chroma_storage_db(self, chunks: List[Dict[str, Any]]) -> ChromaStorage:
        """
        Store chunks in ChromaDB
        
        Args:
            chunks (List[Dict[str, Any]]): Chunks to store
            
        Returns:
            ChromaStorage: Storage instance
        """
        self.storage = ChromaStorage(data=chunks)
        return self.storage.storage_db_vector()

    def search_engine(self, query: str, k: int = 5) -> List[Any]:
        """
        Search the vector store for relevant documents
        
        Args:
            query (str): Search query
            k (int): Number of results to return
            
        Returns:
            List[Any]: Search results
        """
        if self.storage is None:
            raise ValueError("Vector store not initialized. Call chroma_storage_db first.")
        vectorstore = self.storage.storage_db_vector()
        return self.storage.query_top_k(vectorstore=vectorstore, query=query, k=k)

    def chatgpt_response_to_html(self, response_text: str) -> str:
        """
        Convert markdown response to HTML
        
        Args:
            response_text (str): Markdown text
            
        Returns:
            str: HTML formatted text
        """
        return markdown.markdown(response_text)

def setup_pipeline(data_path: str) -> RagPipeline:
    """
    Set up and initialize the RAG pipeline
    
    Args:
        data_path (str): Path to the data directory
        
    Returns:
        RagPipeline: Initialized pipeline
    """
    pipeline = RagPipeline(data_path=data_path)
    metadata = pipeline.extract_data()
    chunks = pipeline.semantic_chunk(metadata)
    pipeline.chroma_storage_db(chunks)
    return pipeline

# Initialize the pipeline
PIPELINE = setup_pipeline("/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/doctor_advice/storage")

def mainChat(
    chatHistoryCache: Optional[str] = None,
    medical_db: Optional[str] = None,
    question: str = None
) -> str:
    print(question)
    try:
        # Validate input
        # if not question.strip():
        #     return "Vui lòng nhập câu hỏi"

        # Search for relevant documents
        start_time = time.time()
        results = PIPELINE.search_engine(question)
        chunk_text = "".join(str(doc.metadata) for doc in results)
        print("time search engine",time.time() - start_time)
        # Format system prompt
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            medical_db=medical_db or "Không có thông tin",
            chunk_text=chunk_text,
            chatHistoryCache=chatHistoryCache or "Không có lịch sử chat",
            question=question
        )

        # # Initialize Gemini Pro 1.5
        # llm = ChatGoogleGenerativeAI(
        #     model="gemini-1.5-pro",
        #     temperature=1,
        #     top_p=0.9,
        #     google_api_key="AIzaSyBoLp2fXcrGICLQHUY4YyKv3jvujbqypSo"  # Thay thế bằng API key của bạn
        # )
        

        # # Create messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]

        # Get response from Gemini
        start_time = time.time()
        # response = llm.invoke(messages)
        response = client.chat.completions.create(
            messages= messages,
            temperature=1.0,
            top_p=1.0,
            max_tokens=4000,
            model=model_name
        )
        print("time llm",time.time() - start_time)

        # Convert response to HTML
        # result = PIPELINE.chatgpt_response_to_html(
        #     response_text=response.content
        # )
        result = PIPELINE.chatgpt_response_to_html(
            response_text=response.choices[0].message.content
        )
        return result

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
        return "Xin lỗi, đã có lỗi xảy ra trong quá trình xử lý. Vui lòng thử lại sau."
