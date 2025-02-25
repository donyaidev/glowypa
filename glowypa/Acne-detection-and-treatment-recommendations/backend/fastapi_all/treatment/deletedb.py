from elasticsearch import Elasticsearch
import time

def init_elasticsearch():
    # Connect to Elasticsearch
    es = Elasticsearch("http://localhost:9200")
    
    # Wait for Elasticsearch to start
    while not es.ping():
        print("Waiting for Elasticsearch...")
        time.sleep(3)
    
    print("Elasticsearch is running!")
    
    # Delete all existing indices
    try:
        es.indices.delete(index='treatment_data')
        print("All indices deleted")
    except:
        print("No indices to delete")
    
if __name__ == "__main__":
    init_elasticsearch()
