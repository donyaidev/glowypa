# import os
# from openai import OpenAI
# from dotenv import load_dotenv
# from search_db import ElasticSearchDB
# load_dotenv()
# token = os.getenv('GITHUB_TOKEN')



# def treatment_gpt(question, retrieval_data):  
#     endpoint = "https://models.inference.ai.azure.com"
#     model_name = "gpt-4o-mini"

#     client = OpenAI(
#         base_url=endpoint,
#         api_key=token,
#     )

#     response = client.chat.completions.create(
#         messages=[
#             {"role": "system", "content": "Bạn là trợ lý thông tin y tế. Glowypa Vui lòng cung cấp thông tin dựa trên bằng chứng từ các nguồn đáng tin cậy. trả lời bằng tiếng anh"},
#             {
#                 "role": "user", "content": f"""
#                 Dựa trên dữ liệu healthcare tham khảo sau:
#                 {retrieval_data}

#                 Câu hỏi: {question}

#                 Vui lòng cung cấp bản tóm tắt thông tin y tế chuyên nghiệp.
                
#                 """
#             }
#         ],
#         temperature=1.0,
#         top_p=1.0,
#         max_tokens=4000,
#         model=model_name
#     )
#     return response.choices[0].message.content

# if __name__ == "__main__":
#     search = ElasticSearchDB()
#     question = "Which treatments are recommended for acne in pregnancy?"
#     retrieval_data = search.multi_vector_search(query_text=question)
#     retrieval_sys = ""
#     arr = []
#     for item in retrieval_data:
#         arr.append(item["Text"])
#         retrieval_sys +=" "+item["Text"]
#     print(arr)
#     print("answer:", treatment_gpt(question, retrieval_data=retrieval_sys))