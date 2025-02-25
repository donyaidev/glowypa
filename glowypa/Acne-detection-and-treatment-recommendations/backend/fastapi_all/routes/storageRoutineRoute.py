from fastapi import APIRouter, HTTPException
from models.storage_routine_table import RecommendMessage
from config.database import routine_favourit_table
from bson import ObjectId
from typing import List, Dict, Any
from fastapi.responses import JSONResponse

# Initialize the router
storage_routine = APIRouter()

def sanitize_mongodb_doc(data: Any) -> Dict:
    """
    Sanitize MongoDB document by converting ObjectId to string and handling nested documents
    """
    if isinstance(data, dict):
        # Create a new dict to avoid modifying the original
        sanitized = {}
        for key, value in data.items():
            if key == "_id":
                sanitized["id"] = str(value)
            else:
                # Recursively sanitize nested documents
                sanitized[key] = sanitize_mongodb_doc(value)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_mongodb_doc(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

def validate_object_id(id: str) -> ObjectId:
    """
    Validate and convert string ID to ObjectId
    """
    try:
        return ObjectId(id)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID format. Must be a 24-character hex string."
        )

@storage_routine.post("/api/v1/storage-recommend-message/", response_model=List[Dict])
async def save_recommend_message(recommend_message: RecommendMessage) -> List[Dict]:
    try:
        # Convert Pydantic model to dict and exclude None values
        data = recommend_message.dict(by_alias=True, exclude_none=True)
        
        # Insert document
        result = routine_favourit_table.insert_one(data)
        
        # Retrieve the inserted document
        saved_message = routine_favourit_table.find_one({"_id": result.inserted_id})
        if not saved_message:
            raise HTTPException(status_code=500, detail="Failed to retrieve saved message")
        
        # Sanitize and return the document
        return [sanitize_mongodb_doc(saved_message)]
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save recommend message: {str(e)}"
        )

@storage_routine.get("/api/v1/storage-recommend-messages/{user_id}", response_model=List[Dict])
async def get_all_recommend_messages_by_user_id(user_id: str) -> List[Dict]:
    try:
        # Find all messages for the user
        recommend_messages = list(routine_favourit_table.find({"user_id": user_id}))
        
        if not recommend_messages:
            return []  # Return empty list instead of 404 error
        
        # Sanitize and return the documents
        return sanitize_mongodb_doc(recommend_messages)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve recommend messages: {str(e)}"
        )

@storage_routine.delete("/api/v1/storage-recommend-message/{id}/{user_id}", response_model=List[Dict])
async def delete_recommend_message(id: str, user_id: str) -> List[Dict]:
    try:
        # Validate ID format
        object_id = validate_object_id(id)
        
        # Delete document
        result = routine_favourit_table.delete_one({
            "_id": object_id,
            "user_id": user_id  # Add user_id check for security
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="RecommendMessage not found or unauthorized"
            )
        
        # Get remaining messages
        remaining_messages = list(routine_favourit_table.find({"user_id": user_id}))
        
        # Sanitize and return the documents
        return sanitize_mongodb_doc(remaining_messages)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete recommend message: {str(e)}"
        )
