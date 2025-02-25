from fastapi import APIRouter, HTTPException, Depends, Header
from models.user_table import UserTable, UserUpdateRequest, LoginRequest
from config.database import user_table
from bson import ObjectId
from schema.schemaUser import userFormat
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from routes.tokenFunction import generate_token, verify_token
user = APIRouter()

SECRET_KEY = "domoraduocpass"
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 1

@user.post("/api/user/login/")
async def login_user(data: LoginRequest):
    print(data)
    user_data = user_table.find_one({"email": data.email})
    if user_data and bcrypt.checkpw(data.password.encode('utf-8'), user_data["password"].encode('utf-8')):
        token = generate_token(data.email)
        return {"message": "login success", "token": token, "data": userFormat(user_data)}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@user.post("/api/user/register/")
async def create_user(user: UserTable):
    existing_user = user_table.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="email already exists")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password = hashed_password
    
    result = user_table.insert_one(dict(user))
    inserted_user = user_table.find_one({"_id": result.inserted_id})
    try:
        return {"message": "User has been created successfully", "user": userFormat(inserted_user)}
    except Exception as e:
        raise HTTPException(status_code=400, detail="failed to create user")

@user.put("/api/user/update/")
async def update_user(user: UserUpdateRequest, token: Optional[str] = Header(None)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token missing")
    
    payload = verify_token(token)
    user_id = ObjectId(user.user_id)
    user_data = user_table.find_one({"_id": user_id, "email": payload["email"]})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user.dict(exclude_unset=True, exclude={"user_id"})
    if "email" in update_data:
        existing_user = user_table.find_one({"email": update_data["email"], "_id": {"$ne": user_id}})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already in use")
    
    result = user_table.update_one({"_id": user_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made to the user")
    
    return {"message": "User has been updated successfully"}
