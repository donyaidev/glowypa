import os
from openai import OpenAI
from dotenv import load_dotenv
from treatment.search_db import ElasticSearchDB
import markdown
import logging
load_dotenv()
import json
import re
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import numpy as np
import torch

import requests


class TreatmentChat:
    def __init__(self):
        self.search = ElasticSearchDB()
        self._token = os.getenv('GITHUB_TOKEN')
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "gpt-4o"
        self.function_definition = [{
                                    "name": "process_medical_question",
                                    "description": "Xử lý câu hỏi liên quan đến vấn đề mụn và trả về định dạng markdown và trả lời chính xác nhât",
                                    "parameters": {
                                        "type": "object",
                                        "properties": {
                                            "answer": {
                                                "type": "string",
                                                "description": "Hãy trả lời câu hỏi dưới dạng markdown"
                                            },
                                            "question_related_acne_medical": {
                                                "type": "boolean",
                                                "description": "Xác định QUESTION có liên quan đến vấn đề mụn, y tế hay không"
                                            }
                                        },
                                        "required": ["answer", "question_related_acne_medical"]
                                    }
                                }]


    def embeddding_calling(self, input_data: str):
        # url_call = "http://0.0.0.0:8888/get_embedding"
        print("hihi")
        url_call = "http://acne-detection-and-treatment-recommendations-embedding-1:8888/get_embedding"

        try:
            response = requests.post(url_call, json={"text": input_data})
            if response.status_code == 200:
                embeddding_text = response.json()['embedding']
                return np.array(embeddding_text)
        except BaseException as e:
            logging.error(f"Error: {e}")
            
    def embedding_callings(self, input_data: list):
        url_call = "http://acne-detection-and-treatment-recommendations-embedding-1:8888/get_embeddings"  
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
        
    def treatment_gpt_acne_detect(self, question, history_chat, medical_db, retrieval_data):
        client = OpenAI(
            base_url=self.endpoint,
            api_key=self._token,
        )
        print("question: ", question)
        print("retrieval_data: ", retrieval_data)
        print("medical_db: ",medical_db)
        print("all_qs", f"""
            **Patient Information:**
            - **QUESTION:** {question}
            - **Clinical Data:** {retrieval_data}
            - **Medical Records:** {medical_db}

            **Consultation Request:**
            Please conduct a thorough dermatological assessment and provide a detailed consultation covering the following:

            1. **Clinical Assessment:**
            - Primary diagnosis and acne classification.
            - Evaluation of clinical manifestations and symptoms.
            - Severity assessment using standard dermatological scales.
            - Analysis of potential underlying causes and triggers.

            2. **Treatment Protocol:**
            - First-line treatment recommendations.
            - Topical medication options and proper application guidelines.
            - Systemic treatment considerations (if applicable).
            - Expected treatment course, prognosis, and follow-up schedule.

            3. **Comprehensive Care Plan:**
            - Evidence-based skincare regimen.
            - Lifestyle modifications and dietary recommendations.
            - Management of environmental factors and preventive measures.

            4. **Medical Considerations:**
            - Contraindications and drug interactions.
            - Management of potential adverse effects.
            - Identification of red flags requiring immediate medical attention.
            - Emphasis on treatment compliance and monitoring.

            **Clinical Guidelines:**
            - Follow current dermatological practice standards.
            - Provide personalized, evidence-based recommendations.
            - Ensure clear explanations with professional terminology.
            - Highlight necessary precautions, monitoring, and referrals (if needed).

            **Note:** Please respond in Vietnamese and tailor all recommendations to align with standard medical protocols and patient-specific factors.
            Bạn là chuyên gia điều trị mụn. Hãy trả lời với đầy đủ các trường dữ liệu:
            - **answer**: Câu trả lời chi tiết.
            - **question_related_acne_medical**: Xác định câu hỏi có liên quan đến vấn đề mụn y tế hay không (True/False).
            Hãy trả lời phù hợp trong 4000 token
            """)
        response = client.chat.completions.create(
            messages=[
            {"role": "system", "content": """You are Dr. Glowypa, a board-certified dermatologist with extensive experience in treating acne and skin conditions. Provide professional, empathetic, and evidence-based dermatological consultations"""},
            {
            "role": "user", 
            "content": f"""
            **Patient Information:**
            - **QUESTION:** {question}
            - **Clinical Data:** {retrieval_data}
            - **Medical Records:** {medical_db}

            **Consultation Request:**
            Please conduct a thorough dermatological assessment and provide a detailed consultation covering the following:

            1. **Clinical Assessment:**
            - Primary diagnosis and acne classification.
            - Evaluation of clinical manifestations and symptoms.
            - Severity assessment using standard dermatological scales.
            - Analysis of potential underlying causes and triggers.

            2. **Treatment Protocol:**
            - First-line treatment recommendations.
            - Topical medication options and proper application guidelines.
            - Systemic treatment considerations (if applicable).
            - Expected treatment course, prognosis, and follow-up schedule.

            3. **Comprehensive Care Plan:**
            - Evidence-based skincare regimen.
            - Lifestyle modifications and dietary recommendations.
            - Management of environmental factors and preventive measures.

            4. **Medical Considerations:**
            - Contraindications and drug interactions.
            - Management of potential adverse effects.
            - Identification of red flags requiring immediate medical attention.
            - Emphasis on treatment compliance and monitoring.

            **Clinical Guidelines:**
            - Follow current dermatological practice standards.
            - Provide personalized, evidence-based recommendations.
            - Ensure clear explanations with professional terminology.
            - Highlight necessary precautions, monitoring, and referrals (if needed).

            **Note:** Please respond in Vietnamese and tailor all recommendations to align with standard medical protocols and patient-specific factors.
            Bạn là chuyên gia điều trị mụn. Hãy trả lời với đầy đủ các trường dữ liệu:
            - **answer**: Câu trả lời chi tiết.
            - **question_related_acne_medical**: Xác định câu hỏi có liên quan đến vấn đề mụn y tế hay không (True/False).
            Hãy trả lời phù hợp trong 4000 token
            """
            }
        ],

            temperature=0.1,
            top_p=0.1,
            presence_penalty=0.1,
            frequency_penalty=0.1,
            max_tokens=8000,
            functions= self.function_definition,
            function_call={"name": "process_medical_question"},
            stop=["Note:", "Warning:", "Caution:"],
            model=self.model_name
        )
        print(response.choices[0].message.function_call)
        args = response.choices[0].message.function_call.arguments
        # args = args.strip()
        # args = args.replace('\n', '\\n')
        # args = self.remove_newlines(args)
        # args = self.clean_json_string(args)
        # print(args)
        return json.loads(args)

    
    def treatment_gpt(self, question, history_chat,medical_db, retrieval_data):  
        client = OpenAI(
            base_url=self.endpoint ,
            api_key=self._token,
        )
        print("retrieval_data", retrieval_data)
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "System: You are Glowypa Doctor chatbot, a skincare information assistant."},
                {
                "role": "user",
                "content": f"""
                Based on the following information, please provide professional medical advice:

                QUESTION:
                {question}

                RETRIEVAL DATA:
                {retrieval_data}

                CHAT HISTORY:
                {history_chat}
                Bạn là chuyên gia điều trị mụn. Hãy trả lời với đầy đủ các trường dữ liệu:
                - **answer**: Câu trả lời chi tiết.
                - **question_related_acne_medical**: Xác định câu hỏi có liên quan đến vấn đề mụn y tế hay không (True/False).
                Bạn là chuyên gia điều trị mụn, hãy tập trung vào câu hỏi trả lời đúng trọng tâm và dễ hiểu
                Hãy trả lời phù hợp trong 4000 token
                """
            }
            ],
            temperature=0.1,
            top_p=0.1,
            presence_penalty = 0.1,
            frequency_penalty = 0.1,
            max_tokens=8000,
            functions=self.function_definition,
            function_call={"name": "process_medical_question"},
            stop = ["Lưu ý:", "Cảnh báo:", "Chú ý:"],
            model=self.model_name
        )
        print(response.choices[0].message.function_call)
        args = response.choices[0].message.function_call.arguments
        # args = args.strip()  # Xóa khoảng trắng thừa
        # args = args.replace('\n', '\\n')  # Escape newlines
        # args = self.remove_newlines(args)
        # args = self.clean_json_string(args)
        print(args)
        return json.loads(args)
    
    def clean_json_string(self, json_str):
        """
        Làm sạch và sửa chữa chuỗi JSON không hoàn chỉnh
        """
        # Xóa bỏ khoảng trắng thừa
        json_str = json_str.strip()
        
        # Kiểm tra xem có phải JSON object không hoàn chỉnh
        if json_str.startswith('{"') and not json_str.endswith('}'):
            # Tìm key cuối cùng
            last_key_start = json_str.rfind('{"')
            if last_key_start != -1:
                # Lấy phần nội dung sau key cuối
                content = json_str[last_key_start:]
                # Đóng JSON object
                if content.endswith('\n'):
                    content = content.rstrip('\n') + '"}'
                elif not content.endswith('"}'):
                    content = content + '"}'
                return content
        return json_str
    
    def chatgpt_response_to_html(self, response_text):
        # Chuẩn hóa khoảng trống và xuống dòng
        # response_text = re.sub(r'\n{3,}', '\n\n', response_text)
        # response_text = re.sub(r'(?<=\d\.)\s*', ' ', response_text)
        
        # html_output = markdown.markdown(
        #     response_text,
        #     extensions=[
        #         'markdown.extensions.extra',
        #         'markdown.extensions.nl2br',
        #         'markdown.extensions.sane_lists'
        #     ]
        # )
        
        # # Wrap trong div với class để style
        # html_output = f'<div>{html_output}</div>'
        # return html_output
        return response_text
    
    def remove_newlines(self, input_string):
        """
        Remove newlines from a string and normalize spaces
        """
        if not isinstance(input_string, str):
            input_string = str(input_string)
        # Remove newlines and normalize spaces
        cleaned = input_string.replace('\n', ' ').replace('\r', ' ')
        # Remove multiple spaces
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
    def get_top_similar_sentences(self, sentences, question: str, top_n: int = 2):
        # Handle empty input cases
        if len(sentences) <= 2:
            texts = ""
            for text in sentences:
                texts += " "+text
            return texts
        
        # Convert inputs to lists if they're not already
        question_list = [question] if isinstance(question, str) else question
        sentences_list = sentences if isinstance(sentences, list) else [sentences]
        
        try:
            # Generate embeddings
            question_embedding = self.embedding_callings(input_data=question_list)
            sentence_embeddings = self.embedding_callings(input_data=sentences_list)
            
            # Debug prints
            print("Question embedding shape:", question_embedding.shape)
            print("Sentence embeddings shape:", sentence_embeddings.shape)
            
            # Convert to PyTorch tensors if they aren't already
            if not isinstance(question_embedding, torch.Tensor):
                question_embedding = torch.tensor(question_embedding)
            if not isinstance(sentence_embeddings, torch.Tensor):
                sentence_embeddings = torch.tensor(sentence_embeddings)
                
            # Convert to float32
            question_embedding = question_embedding.float()
            sentence_embeddings = sentence_embeddings.float()
            
            # Reshape tensors to proper dimensions
            if len(question_embedding.shape) == 1:
                question_embedding = question_embedding.unsqueeze(0)
            if len(sentence_embeddings.shape) == 1:
                sentence_embeddings = sentence_embeddings.unsqueeze(0)
                
            # Calculate cosine similarity
            cosine_scores = torch.nn.functional.cosine_similarity(
                question_embedding.unsqueeze(0),
                sentence_embeddings.unsqueeze(1),
                dim=2
            )
            
            # Convert to numpy and ensure it's 1-dimensional
            cosine_scores = cosine_scores.squeeze().detach().numpy()
            if np.isscalar(cosine_scores):
                cosine_scores = np.array([cosine_scores])
            
            # Adjust top_n if it's larger than the number of sentences
            top_n = min(top_n, len(sentences_list))
            
            # Get top results
            top_indices = np.argsort(cosine_scores)[::-1][:top_n]
            
            results = ''
            for idx in top_indices:
                results += " "+sentences_list[idx]
            return results
            
        except Exception as e:
            print(f"Error in get_top_similar_sentences: {str(e)}")
            print(f"Question: {question}")
            print(f"Sentences length: {len(sentences_list)}")
            if 'cosine_scores' in locals():
                print(f"Cosine scores shape: {cosine_scores.shape if hasattr(cosine_scores, 'shape') else 'scalar'}")
            raise

    def generate_references_markdown(self, reference_docs):
        """
        Convert a list of reference documents into a Markdown-formatted string.
        
        Args:
            reference_docs (list): A list of dictionaries with keys 'file_name', 'page', and optionally 'score'.
            
        Returns:
            str: A Markdown-formatted string of references.
        """
        markdown = "### References:\n\n"
        for i, item in enumerate(reference_docs, start=1):
            file_name = item.get("file_name", "Unknown File")
            page = item.get("page", "Unknown Page")
            score = item.get("score", None)
            
            # Format the reference with or without the score
            if score is not None:
                markdown += f"[{i}] **{file_name}** - Page: {page} \n\n"
            else:
                markdown += f"[{i}] **{file_name}** - Page: {page} \n\n"
        
        return markdown
    
    def advice_treatment_chat(self, question, chatHistoryCache=None, medical_db=None):
        history_chat = self.get_top_similar_sentences(question=question, sentences = chatHistoryCache)
        print(medical_db)
        try:
            elastic_search_retrieval = self.search.multi_vector_search(query_text=question)
            reference_docs = [{"file_name":item["file_name"], "page":item["page"], "score":item["score"]} for item in elastic_search_retrieval]
            markdown_output = self.generate_references_markdown(reference_docs)
            retrieval_sys = " ".join(item["text"] for item in elastic_search_retrieval)
            answer = self.treatment_gpt(question, history_chat, medical_db,retrieval_data=retrieval_sys)
            markdown_message = self.chatgpt_response_to_html(answer["answer"])
            markdown_message = answer["answer"]
            logger.debug("answer")
            if answer.get("question_related_acne_medical", True) == True: 
                return {"message": markdown_message + "\n\n" + markdown_output, "doc_reference": reference_docs, "question_related_acne_medical": True }
            return {"message": markdown_message, "doc_reference": reference_docs, "question_related_acne_medical": answer["question_related_acne_medical"] }
        except Exception as e:
            logger.error(f"Error during chat invocation1: {e}")
            return {"message": "The response was filtered due to the prompt triggering Glowypa and Azure OpenAI's content management policy. Please modify your prompt and retry. ", "doc_reference": [], "question_related_acne_medical": False}
    
    def advice_treatment_chat_acne_detect(self, question, chatHistoryCache=None, medical_db=None):
        # history_chat = self.get_top_similar_sentences(question=question, sentences = chatHistoryCache)
        history_chat = 'No'
        try:
            elastic_search_retrieval = self.search.multi_vector_search(query_text=medical_db)
            print("eksdb: ",elastic_search_retrieval)
            reference_docs = [{"file_name":item["file_name"], "page":item["page"], "score":item["score"]}for item in elastic_search_retrieval]
            markdown_output = self.generate_references_markdown(reference_docs)
            retrieval_sys = " ".join(item["text"] for item in elastic_search_retrieval)
            answer = self.treatment_gpt_acne_detect(question, history_chat, medical_db,retrieval_data=retrieval_sys)
            markdown_message = self.chatgpt_response_to_html(answer["answer"])
            markdown_message = answer["answer"]
            if answer.get("question_related_acne_medical", True) == True: 
                return {"message": markdown_message + "\n\n" + markdown_output, "doc_reference": reference_docs, "question_related_acne_medical": answer["question_related_acne_medical"] }
            return {"message": markdown_message, "doc_reference": reference_docs, "question_related_acne_medical": answer["question_related_acne_medical"] }

        except Exception as e:
            logger.error(f"Error during chat invocation2: {e}")
            return {"message": "The response was filtered due to the prompt triggering Glowypa and Azure OpenAI's content management policy. Please modify your prompt and retry. ", "doc_reference": [], "question_related_acne_medical": False}


