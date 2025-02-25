from elasticsearch import Elasticsearch
import numpy as np
import logging
import requests
class ElasticSearchDB:
    def __init__(self):
        # self._es = Elasticsearch("http://localhost:9200")
        self._es = Elasticsearch("http://acne-detection-and-treatment-recommendations-elasticdb-1:9200")
    def embeddding_calling(self, input_data: str):
        print("searchdb")
        # url_call = "http://0.0.0.0:8888/get_embedding"
        url_call = "http://acne-detection-and-treatment-recommendations-embedding-1:8888/get_embedding"

        try:
            response = requests.post(url_call, json={"text": input_data})
            if response.status_code == 200:
                embeddding_text = response.json()['embedding']
                return np.array(embeddding_text)
        except BaseException as e:
            logging.error(f"Error: {e}")


    def query_all(self):
        try:
            response = self._es.search(
            index="treatment_data",
            body={
                "query": {
                    "match_all": {}
                },
                "size": 10000
                }
            )
            print(len(response['hits']['hits']))
        except Exception as e:
            logging.error('error: ', e)
            
    def query_by_file_name(self, file_name):
        try:
            response = self._es.search(
                        index="treatment_data",
                        body={
                            "query": {
                                "term": {
                                    "file_name.keyword": file_name  # Dùng .keyword để tìm kiếm chính xác
                                }
                            },
                            "size": 10000  # Giới hạn số lượng kết quả trả về
                        }
                    )
            # Lấy danh sách kết quả
            hits = response['hits']['hits']
            total_hits = len(hits)  # Tổng số lượng kết quả
            print(total_hits)
        except Exception as e:
            logging.error('Error occurred: ', exc_info=True)
            
    def query_match(self,query_text = "Salicylic Acid"):
        try:
            response = self._es.search(
                index="treatment_data",
                body={
                    "query": {
                        "match": {
                            "text": query_text 
                        }
                    },
                    "size": 10000 
                }
            )
            hits = response['hits']['hits']
            for hit in hits:
                print(f"ID: {hit['_id']}, Score: {hit['_score']}, Source: {hit['_source']}")
            
            print(f"Tổng số kết quả: {len(hits)}")
        except Exception as e:
            logging.error('Error: ', exc_info=True)        

    def multi_vector_search(self,query_text):
        try:
            query_embedding = self.embeddding_calling(query_text)
            response = self._es.search(
                index='treatment_data',
                body={
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": """
                                    // Tính cosine similarity
                                    cosineSimilarity(params.query_vector, 'embedding') + 1.0
                                """,
                                "params": {
                                    "query_vector": query_embedding.tolist()
                                }
                            }
                        }
                    },
                    "size": 5  
                }
            )
            hits = response['hits']['hits']
            retrieval_data = []
            for hit in hits:
                retrieval_data.append({
                    "file_name": hit['_source']['file_name'],
                    "page": hit['_source']['page'],
                    "score": hit['_score'],
                    "text": hit['_source']['text']
                })
            if retrieval_data:
                return retrieval_data
            else:
                return [{
                    "File": "",
                    "Page":"",
                    "Score": "",
                    "text": ""
                }]
        except Exception as e:
            print(f"Error: {e}")
            return [{
                "File": "",
                "Page":"",
                "Score": "",
                "text": ""
            }]

if __name__ == "__main__":
    search = ElasticSearchDB()
    # data = search.multi_vector_search("mụn mủ")
    # print(data)
    search.query_by_file_name("Treatment of Acne Scars.pdf")
    # query_match()