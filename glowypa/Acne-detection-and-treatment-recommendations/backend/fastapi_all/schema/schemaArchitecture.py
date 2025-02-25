from datetime import datetime

def architectureFormat(architecture) -> dict:
    return {
        "id": str(architecture['_id']),
        "ai_name": architecture['ai_name'],
        "ai_description": architecture['ai_description']
    }
    
def architecturesFormat(architectures) -> dict:
    return [architectureFormat(architecture) for architecture in architectures]