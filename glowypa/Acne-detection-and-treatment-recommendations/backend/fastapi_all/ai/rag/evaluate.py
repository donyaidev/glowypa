# Import các thư viện cần thiết
from langchain_community.chat_models import ChatOllama
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from doctor_advice.db.chromaRag import ChromaStorage
from doctor_advice.extract_data.document_convert import ExtractData
from doctor_advice.extract_data.semantic_chunking import SemanticChunker
from typing import List, Dict, Any, Optional, Tuple
import os
import ollama
import markdown
import time
import numpy as np
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from openai import OpenAI
from decimal import Decimal

# Cấu hình OpenAI
token = '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'
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Định nghĩa system prompt
SYSTEM_PROMPT_TEMPLATE = """ trả lời đúng trọng tâm
"""

class RagPipeline:
    def __init__(self, data_path: str) -> None:
        self.data_path = data_path
        self.extractor = ExtractData()
        self.chunker = SemanticChunker(chunk_size=500, chunk_overlap=50)
        self.storage = None

    def extract_path(self, data_path: str) -> List[str]:
        files = os.listdir(data_path)
        return [os.path.join(data_path, file) for file in files]

    def extract_data(self) -> List[Dict[str, Any]]:
        return [self.extractor.text_from_pdf(path) for path in self.extract_path(self.data_path)]

    def semantic_chunk(self, metadata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return self.chunker.semantic_chunking_process(metadata)

    def chroma_storage_db(self, chunks: List[Dict[str, Any]]) -> ChromaStorage:
        self.storage = ChromaStorage(data=chunks)
        return self.storage.storage_db_vector()

    def search_engine(self, query: str, k: int = 5) -> List[Any]:
        if self.storage is None:
            raise ValueError("Vector store not initialized. Call chroma_storage_db first.")
        vectorstore = self.storage.storage_db_vector()
        return self.storage.query_top_k(vectorstore=vectorstore, query=query, k=k)

    def chatgpt_response_to_html(self, response_text: str) -> str:
        return markdown.markdown(response_text)

class RAGEvaluator:
    def __init__(self, pipeline: RagPipeline):
        self.pipeline = pipeline
        self.test_questions = [
            "Mụn bọc (cystic acne) có đặc điểm gì?",
            # "Tại sao blackheads có màu đen trong khi whiteheads có màu trắng? Cơ chế hình thành của chúng khác nhau như thế nào?",
            # "Trong trường hợp bị mụn conglobata, tại sao bác sĩ thường kê đơn isotretinoin và cần theo dõi chặt chẽ những gì?",
            # "Làm thế nào để phân biệt giữa mụn nang (cystic acne) và mụn conglobata? Các phương pháp điều trị của chúng có gì khác nhau?",
            # "Khi nào nên sử dụng liệu pháp hormone trong điều trị mụn và đối tượng nào phù hợp với phương pháp này?",
            # "Tại sao mụn cóc phẳng (flat wart) thường xuất hiện thành cụm và các phương pháp điều trị nào hiệu quả nhất?",
            # "Trong trường hợp bị viêm nang lông (folliculitis), tại sao việc cạo râu không được khuyến khích và nên áp dụng những biện pháp thay thế nào?",
            # "Sẹo keloid và sẹo phì đại (hypertrophic scars) có điểm gì khác nhau? Phương pháp điều trị nào phù hợp cho từng loại?",
            # "Tại sao milia thường xuất hiện quanh vùng mắt và má? Có cần thiết phải điều trị chúng không?",
            # "Trong điều trị papule, tại sao việc kết hợp benzoyl peroxide và salicylic acid được khuyến nghị? Cơ chế hoạt động của chúng như thế nào?"
        ]

    def measure_response_time(self, question: str) -> Tuple[float, str]:
        start_time = time.time()
        response = mainChat(question=question)
        end_time = time.time()
        return end_time - start_time, response

    def evaluate_faithfulness(self, question: str, response: str) -> Tuple[float, List[str]]:
        """
        Evaluates the faithfulness of a response by comparing it with relevant documents.
        
        Args:
            question (str): The input question
            response (str): The generated response to evaluate
            
        Returns:
            Tuple[float, List[str]]: A tuple containing:
                - faithfulness score (float between 0 and 1)
                - list of matching content from source documents
        """
        print(response)
        try:
            # Input validation
            if not question or not response:
                return 0.0, []
                
            # Get relevant documents
            relevant_docs = self.pipeline.search_engine(question)
            if not relevant_docs:
                return 0.0, []

            # Initialize scoring variables
            matching_content = []
            score = 0
            
            # Process each document
            for doc in relevant_docs:
                # Extract content from both metadata and page_content
                doc_content = []
                
                if doc.metadata:
                    doc_content.extend(self._extract_points(str(doc.metadata)))
                
                if doc.page_content:
                    doc_content.extend(self._extract_points(doc.page_content))
                
                # Check for matching content
                response_lower = response.lower()
                for point in doc_content:
                    if point.lower() in response_lower:
                        score += 1
                        matching_content.append(point)
            
            # Calculate faithfulness score
            total_docs = len(relevant_docs) if relevant_docs else 1
            faithfulness_score = Decimal(score) / Decimal(total_docs)
            
            return float(faithfulness_score), list(set(matching_content))  # Remove duplicates
            
        except Exception as e:
            return 0.0, []

    def evaluate_relevancy(self, question: str, response: str) -> Tuple[float, Dict]:
        relevant_docs = self.pipeline.search_engine(question)
        keywords = set(question.lower().split())
        
        details = {
            'keyword_overlap': 0,
            'context_coverage': 0,
            'answer_completeness': 0
        }
        
        response_words = set(response.lower().split())
        keyword_overlap = len(keywords & response_words) / len(keywords)
        details['keyword_overlap'] = keyword_overlap
        
        doc_content = ' '.join([str(doc.metadata) for doc in relevant_docs])
        doc_words = set(doc_content.lower().split())
        context_coverage = len(response_words & doc_words) / len(doc_words)
        details['context_coverage'] = context_coverage
        
        expected_keywords = {'mụn', 'điều trị', 'nguyên nhân', 'cách', 'phương pháp'}
        completeness = len(response_words & expected_keywords) / len(expected_keywords)
        details['answer_completeness'] = completeness
        
        relevancy_score = (keyword_overlap + context_coverage + completeness) / 3
        return relevancy_score, details

    def run_evaluation(self) -> Dict:
        results = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'questions': [],
            'summary': {}
        }
        
        response_times = []
        faithfulness_scores = []
        relevancy_scores = []
        
        for i, question in enumerate(self.test_questions, 1):
            print(f"\nĐang đánh giá câu hỏi {i}/10: {question}")
            
            response_time, response = self.measure_response_time(question)
            faithfulness_score, matching_content = self.evaluate_faithfulness(question, response)
            relevancy_score, relevancy_details = self.evaluate_relevancy(question, response)
            
            question_result = {
                'question': question,
                'response_time': response_time,
                'faithfulness': {
                    'score': faithfulness_score,
                    'matching_content': matching_content[:3]
                },
                'relevancy': {
                    'score': relevancy_score,
                    'details': relevancy_details
                }
            }
            
            results['questions'].append(question_result)
            
            response_times.append(response_time)
            faithfulness_scores.append(faithfulness_score)
            relevancy_scores.append(relevancy_score)
            
            time.sleep(4)
        
        results['summary'] = {
            'average_response_time': np.mean(response_times),
            'average_faithfulness': np.mean(faithfulness_scores),
            'average_relevancy': np.mean(relevancy_scores),
            'std_response_time': np.std(response_times),
            'std_faithfulness': np.std(faithfulness_scores),
            'std_relevancy': np.std(relevancy_scores)
        }
        
        return results

def setup_pipeline(data_path: str) -> RagPipeline:
    pipeline = RagPipeline(data_path=data_path)
    metadata = pipeline.extract_data()
    chunks = pipeline.semantic_chunk(metadata)
    pipeline.chroma_storage_db(chunks)
    return pipeline

def print_evaluation_results(results: Dict):
    print("\n=== KẾT QUẢ ĐÁNH GIÁ RAG SYSTEM ===")
    print(f"Thời gian đánh giá: {results['timestamp']}")
    print("\nTỔNG KẾT:")
    print(f"- Thời gian phản hồi trung bình: {results['summary']['average_response_time']:.2f}s (±{results['summary']['std_response_time']:.2f}s)")
    print(f"- Độ tin cậy trung bình: {results['summary']['average_faithfulness']:.2f} (±{results['summary']['std_faithfulness']:.2f})")
    print(f"- Độ liên quan trung bình: {results['summary']['average_relevancy']:.2f} (±{results['summary']['std_relevancy']:.2f})")
    
    print("\nCHI TIẾT TỪNG CÂU HỎI:")
    for i, q_result in enumerate(results['questions'], 1):
        print(f"\nCâu hỏi {i}: {q_result['question']}")
        print(f"- Thời gian phản hồi: {q_result['response_time']:.2f}s")
        print(f"- Độ tin cậy: {q_result['faithfulness']['score']:.2f}")
        print(f"- Độ liên quan: {q_result['relevancy']['score']:.2f}")
        # print("  + Độ trùng khớp từ khóa: {:.2f}".format(q_result['relevancy']['details']['keyword_overlap']))
        # print("  + Độ bao phủ ngữ cảnh: {:.2f}".format(q_result['relevancy']['details']['context_coverage']))
        # print("  + Độ đầy đủ câu trả lời: {:.2f}".format(q_result['relevancy']['details']['answer_completeness']))

def mainChat(
    chatHistoryCache: Optional[str] = None,
    medical_db: Optional[str] = None,
    question: str = None
) -> str:
    try:
        results = PIPELINE.search_engine(question)
        chunk_text = "".join(str(doc.metadata) for doc in results)

        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            medical_db=medical_db or "Không có thông tin",
            chunk_text=chunk_text,
            chatHistoryCache=chatHistoryCache or "Không có lịch sử chat",
            question=question
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]

        response = client.chat.completions.create(
            messages=messages,
            temperature=0,
            top_p=1.0,
            max_tokens=4000,
            model=model_name
        )

        result = PIPELINE.chatgpt_response_to_html(
            response_text=response.choices[0].message.content
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return "Xin lỗi, đã có lỗi xảy ra" 
    
PIPELINE = setup_pipeline("/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/ai/rag/doctor_advice/storage")
if __name__ == "__main__":
    # Run evaluation
    evaluator = RAGEvaluator(PIPELINE)
    results = evaluator.run_evaluation()
    print_evaluation_results(results)