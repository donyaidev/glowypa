from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from datetime import datetime
import base64
import uuid
from pymongo import MongoClient
from models.acne_detection_table import AcneTreatment, PredictedImage, Image, ImageBase64AndModel, DeleteAndAddBase64Img  # Import the models here
from schema.schemaAcneDetection import acneDetectionFormat, acneDetectionListFormat
from ai.yolo.acne_predict import acnePredictWithYolo, acnePredictWithSahi
from config.database import acne_detection_table
from bson import ObjectId
import tempfile
import os

acneDetection = APIRouter()
@acneDetection.post("/api/acne_detection_daily/{user_id}")
async def create_or_update_upload_files(
    user_id: str,
    data: List[ImageBase64AndModel],
):
    # today_start = datetime.combine(datetime.now().date(), datetime.min.time())
    # today_end = datetime.combine(datetime.now().date(), datetime.max.time())
    acne_treatment = acne_detection_table.find_one({
        "user_id": user_id,
        # "date": {"$gte": today_start, "$lt": today_end}
    })
    if acne_treatment:
        raise HTTPException(status_code=404, detail="Today exist history")
    
    images = []
    predicted_images = []
    for img_data in data:
        if img_data.image_base64.startswith("data:image/png;base64,"):
            base64_string = img_data.image_base64.split(",", 1)[1]
        else:
            base64_string = img_data.image_base64
        image_bytes = base64.b64decode(base64_string)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name
        try:
            predicte_result_sahi = acnePredictWithSahi(temp_file_path)
            predicted_images.append({
                "image_id": img_data.image_id,
                "predicted": predicte_result_sahi['bounding-box'],
                "architecture_ai_name": "YoloV8 with SAHI",
                "total_acnes": len(predicte_result_sahi['bounding-box'])
            })
            predicte_result_yolo = acnePredictWithYolo(temp_file_path)
            predicted_images.append({
                "image_id": img_data.image_id,
                "predicted": predicte_result_yolo['bounding-box'],
                "architecture_ai_name": "YoloV8",
                "total_acnes": len(predicte_result_yolo['bounding-box'])

            })
            images.append({"image_id": img_data.image_id, "image_base64": img_data.image_base64})
        finally:
            os.remove(temp_file_path)
    
    acne_treatment_instance = {
        "user_id": user_id,
        "images": images,
        "predicted_images": predicted_images,
        "date": datetime.now()
    }
    result = acne_detection_table.insert_one(acne_treatment_instance)
    inserted_document = acne_detection_table.find_one({"_id": result.inserted_id})
    return {"data": acneDetectionFormat(inserted_document)}

@acneDetection.put("/api/acne_detection_daily/deleteAndPut/{user_id}")
async def delete_and_put_upload_files(
    user_id: str,
    data: DeleteAndAddBase64Img,
    
):
    # today_start = datetime.combine(datetime.now().date(), datetime.min.time())
    # today_end = datetime.combine(datetime.now().date(), datetime.max.time())
    status_put = False
    acne_treatment = acne_detection_table.find_one({
        "user_id": user_id,
        # "date": {"$gte": today_start, "$lt": today_end}
    })
    
    if not acne_treatment:
        raise HTTPException(status_code=404, detail="Today have no history")

    updated_images = [img for img in acne_treatment.get("images", []) if img["image_id"] not in data.img_id_remove_list]
    updated_predicted_images = [img_predict for img_predict in acne_treatment.get("predicted_images", []) if img_predict["image_id"] not in data.img_id_remove_list]

    images = []
    predicted_images = []
    
    for img_data in data.image_base64_list:
        status_put = True
        if img_data.image_base64.startswith("data:image/png;base64,"):
            base64_string = img_data.image_base64.split(",", 1)[1]
        else:
            base64_string = img_data.image_base64
        image_bytes = base64.b64decode(base64_string)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_bytes)
            temp_file_path = temp_file.name
        try:
            predicte_result_sahi = acnePredictWithSahi(temp_file_path)
            predicted_images.append({
                "image_id": img_data.image_id,
                "predicted": predicte_result_sahi['bounding-box'],
                "architecture_ai_name": "YoloV8 with SAHI",
                "total_acnes": len(predicte_result_sahi['bounding-box'])
            })
            predicte_result_yolo = acnePredictWithYolo(temp_file_path)
            predicted_images.append({
                "image_id": img_data.image_id,
                "predicted": predicte_result_yolo['bounding-box'],
                "architecture_ai_name": "YoloV8",
                "total_acnes": len(predicte_result_yolo['bounding-box'])
            })
            images.append({"image_id": img_data.image_id, "image_base64": img_data.image_base64})
        finally:
            os.remove(temp_file_path)
    
    updated_images.extend(images)
    updated_predicted_images.extend(predicted_images)
    
    acne_detection_table.update_one(
        {"_id": ObjectId(acne_treatment["_id"])},
        {"$set": {"images": updated_images, "predicted_images": updated_predicted_images}}
    )
    
    acne_treatment_new = acne_detection_table.find_one({
        "user_id": user_id,
        # "date": {"$gte": today_start, "$lt": today_end}
    })    
    
    return {"message": "success: Acne detection has been updated successfully", "data": acneDetectionFormat(acne_treatment_new), "status_put": status_put}

@acneDetection.get("/api/acne_detection_daily/{user_id}")
async def get_acne_detection_daily(
    user_id: str,
):
    # today_start = datetime.combine(datetime.now().date(), datetime.min.time())
    # today_end = datetime.combine(datetime.now().date(), datetime.max.time())
    acne_treatment = acne_detection_table.find_one({
        "user_id": user_id,
        # "date": {"$gte": today_start, "$lt": today_end}
    })
    if not acne_treatment:
        return {"message": "success: get acne_detection_daily", "data": []}

    return {"message": "success: get acne_detection_daily", "data": acneDetectionFormat(acne_treatment)}

@acneDetection.get("/api/acne_detection_user_all/{user_id}")
async def get_acne_detection_user_all(
    user_id: str,
):
    acne_treatment = acne_detection_table.find({"user_id": user_id})
    return {"message": "success: get all detection of user", "data": acneDetectionListFormat(acne_treatment)}

