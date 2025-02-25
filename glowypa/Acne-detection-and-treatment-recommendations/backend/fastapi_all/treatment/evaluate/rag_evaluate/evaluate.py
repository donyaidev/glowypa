from typing import List, Dict, Any
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import json
import requests
import logging
logger = logging.getLogger(__name__)

class TextEvaluator:
    def __init__(self):
        # Tải các resources cần thiết
        nltk.download('punkt')
        nltk.download('stopwords')
        # self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.stop_words = set(stopwords.words('english'))
        
    def embedding_calling(self, input_data: list):
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

    def preprocess_text(self, text: str) -> List[str]:
        """Tiền xử lý văn bản"""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens

    def calculate_faithfulness(self, answer: str, context: List[str]) -> float:
        """Tính điểm Faithfulness"""
        context_text = ' '.join(context)
        answer_embedding = self.embedding_calling([answer])
        context_embedding = self.embedding_calling([context_text])
        similarity = cosine_similarity(answer_embedding, context_embedding)[0][0]
        return similarity

    def calculate_factual_correctness(self, answer: str, ground_truth: str) -> float:
        """Tính điểm FactualCorrectness"""
        answer_embedding = self.embedding_calling([answer])
        truth_embedding = self.embedding_calling([ground_truth])
        similarity = cosine_similarity(answer_embedding, truth_embedding)[0][0]
        return similarity

    def calculate_context_recall(self, answer: str, context: List[str]) -> float:
        """Tính điểm ContextRecall"""
        answer_tokens = set(self.preprocess_text(answer))
        context_tokens = set()
        for text in context:
            context_tokens.update(self.preprocess_text(text))
        
        if len(answer_tokens) == 0:
            return 0
        
        matched_tokens = answer_tokens.intersection(context_tokens)
        recall = len(matched_tokens) / len(answer_tokens)
        return recall

    def calculate_context_precision(self, answer: str, context: List[str]) -> float:
        """Calculate Context Precision score"""
        answer_tokens = set(self.preprocess_text(answer))
        context_tokens = set()
        for text in context:
            context_tokens.update(self.preprocess_text(text))
        
        if len(context_tokens) == 0:
            return 0
        
        matched_tokens = answer_tokens.intersection(context_tokens)
        precision = len(matched_tokens) / len(context_tokens)
        return precision

    def calculate_relevancy(self, question: str, answer: str) -> float:
        """Calculate Relevancy score between question and answer"""
        question_embedding = self.embedding_calling([question])
        answer_embedding = self.embedding_calling([answer])
        similarity = cosine_similarity(question_embedding, answer_embedding)[0][0]
        return similarity

    def evaluate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate all metrics"""
        faithfulness_scores = []
        factual_scores = []
        recall_scores = []
        precision_scores = []  # New
        relevancy_scores = []  # New
        
        for i in range(len(data['questions'])):
            answer = data['answers'][i]
            context = data['contexts'][i]
            ground_truth = data['ground_truths'][i]
            question = data['questions'][i]  # Added
            
            faithfulness = self.calculate_faithfulness(answer, context)
            factual = self.calculate_factual_correctness(answer, ground_truth)
            recall = self.calculate_context_recall(answer, context)
            precision = self.calculate_context_precision(answer, context)  # New
            relevancy = self.calculate_relevancy(question, answer)  # New
            
            faithfulness_scores.append(faithfulness)
            factual_scores.append(factual)
            recall_scores.append(recall)
            precision_scores.append(precision)  # New
            relevancy_scores.append(relevancy)  # New
        
        results = {
            'average_metrics': {
                'Faithfulness': np.mean(faithfulness_scores),
                'FactualCorrectness': np.mean(factual_scores),
                'ContextRecall': np.mean(recall_scores),
                'ContextPrecision': np.mean(precision_scores),  # New
                'Relevancy': np.mean(relevancy_scores)  # New
            },
            'individual_scores': {
                'Faithfulness': faithfulness_scores,
                'FactualCorrectness': factual_scores,
                'ContextRecall': recall_scores,
                'ContextPrecision': precision_scores,  # New
                'Relevancy': relevancy_scores  # New
            }
        }
        
        return results


    def print_results(self, results: Dict[str, Any]) -> None:
        """In kết quả đánh giá"""
        print("=== Average Metrics ===")
        for metric, score in results['average_metrics'].items():
            print(f"{metric}: {score:.3f}")
        
        print("\n=== Individual Scores ===")
        num_questions = len(results['individual_scores']['Faithfulness'])
        for i in range(num_questions):
            print(f"\nQuestion {i+1}:")
            for metric in results['individual_scores'].keys():
                score = results['individual_scores'][metric][i]
                print(f"{metric}: {score:.3f}")

# Ví dụ sử dụng:
def main():
    # Giả sử data là biến chứa JSON của bạn
    file_path ="/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/treatment/evaluate/rag_evaluate/test_case_gemini1.5pro_256.json"
    with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
    
    # Khởi tạo evaluator
    evaluator = TextEvaluator()
    
    # Thực hiện đánh giá
    results = evaluator.evaluate(data)
    
    # In kết quả
    evaluator.print_results(results)

if __name__ == "__main__":
    main()
