from datetime import datetime

def feedbackFormat(feedback) -> dict:
    return {
        "id": str(feedback['_id']),
        "user_id": str(feedback['user_id']),
        "image": feedback['image'],
        "feedback_content": feedback['feedback_content'],
        "rate": feedback['rate'],
        "date": feedback['date']
    }
    
def feedbacksFormat(feedbacks) -> dict:
    return [feedbackFormat(feedback) for feedback in feedbacks]