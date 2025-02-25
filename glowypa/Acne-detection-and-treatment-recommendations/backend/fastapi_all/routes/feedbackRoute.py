from fastapi import APIRouter, HTTPException
from models.feedback_table import FeedbackTable, FeedbackPost
from config.database import feedback_table
from bson import ObjectId
from schema.schemaFeedback import feedbackFormat, feedbacksFormat
from datetime import datetime

feedback = APIRouter()

@feedback.get("/api/feedback/")
async def get_all_feedbacks():
    feedbacks = feedback_table.find()
    return feedbacksFormat(feedbacks)

@feedback.get("/api/feedback/{user_id}")
async def get_feedbacks_by_user_id(user_id: str):
    feedbacks = feedback_table.find({"user_id": user_id})
    return feedbacksFormat(feedbacks)

@feedback.post("/api/feedback/")
async def create_feedback(feedback: FeedbackPost):
    data = {
        "user_id": feedback.user_id,
        "image": feedback.image,
        "feedback_content": feedback.feedback_content,
        "rate": feedback.rate,
        "date": datetime.now()
    }
    result = feedback_table.insert_one(data)
    inserted_feedback = feedback_table.find_one({"_id": result.inserted_id})
    return {"message": "Feedback has been created successfully", "feedback": feedbackFormat(inserted_feedback)}