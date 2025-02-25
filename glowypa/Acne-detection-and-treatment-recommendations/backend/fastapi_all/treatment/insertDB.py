from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import numpy as np
import requests
import logging
import uuid
from doctor_advice.extract_data.document_convert import ExtractData
import os
from pathlib import Path
from doctor_advice.extract_data.semantic_chunking import SemanticChunker
import json
from doctor_advice.extract_data.pymue import ExtractTextPDFpyMUPDF
# Kết nối Elasticsearch
es = Elasticsearch("http://localhost:9200")

def embeddding_calling(input_data: str):
    print("insertdb")
    url_call = "http://0.0.0.0:8888/get_embedding"
    try:
        response = requests.post(url_call, json={"text": input_data})
        if response.status_code == 200:
            embeddding_text = response.json()['embedding']
            return np.array(embeddding_text)
    except BaseException as e:
        logging.error(f"Error: {e}")


def insert_data(documents, index_name):
    """
    Insert list of documents into Elasticsearch
    
    documents: List of dictionaries with format:
    {
        'file_name': str,
        'page': str,
        'text': str,
        'embedding': list
    }
    """
    bulk_data = [
        {
            '_index': f'{index_name}',
            '_id': f"{uuid.uuid4()}", 
            '_source': doc
        }
        for doc in documents
    ]
    try:
        success, failed = bulk(es, bulk_data)
        print(f"Documents inserted: {success}")
        if failed:
            print(f"Failed documents: {failed}")
    except Exception as e:
        print(f"Error inserting documents: {str(e)}")

if __name__ == "__main__":
    folder_path= '/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/treatment/doctor_advice/storage'
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
    print(file_paths)
    extractDataPDF = ExtractTextPDFpyMUPDF()
    # extractDataPDF = ExtractData()
    SemanticChunkerProcess = SemanticChunker()
    metadatas = []
    for file_path in file_paths:
        metadatas.extend(SemanticChunkerProcess.semantic_chunking_process([extractDataPDF.extract_text_pdf_pymu(file_path)]))
        # metadatas.extend(SemanticChunkerProcess.semantic_chunking_process([extractDataPDF.text_from_pdf(file_path=file_path)]))
    with open('/home/nhatthuong/Documents/Thesis/Acne-detection-and-treatment-recommendations/backend/fastapi_all/treatment/doctor_advice/json elastic/data.json', 'w', encoding='utf-8') as f:
        json.dump(metadatas, f, ensure_ascii=False, indent=4)
    if metadatas:
        insert_data(metadatas, index_name='treatment_data')
        result = es.count(index="treatment_data")
        print(f"Total documents in index: {result['count']}")
