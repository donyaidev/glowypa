from fastapi import APIRouter, HTTPException, Header, Query
from models.recommend_table import SkincareRoutine, recommendMessage
from config.database import skincare_routine_table
from bson import ObjectId
from typing import Optional, List
from schema.schemaAcneDetection import acneDetectionFormat
from config.database import acne_detection_table
from recommend.recommend_guide import RecommendGuide
recommend = APIRouter()

# Endpoint để admin insert SkincareRoutine
@recommend.post("/api/admin/skincare-routine/insert/")
async def admin_insert_skincare_routine(routine: SkincareRoutine):
    # Thêm routine vào MongoDB
    routine_dict = routine.dict()
    result = skincare_routine_table.insert_one(routine_dict)
    
    if result.inserted_id:
        return {"message": "Skincare routine inserted successfully", "routine_id": str(result.inserted_id)}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert skincare routine")
    
# Endpoint để lấy tất cả skincare routines
@recommend.get("/api/skincare-routine/all/")
async def get_all_skincare_routines():
    routines = list(skincare_routine_table.find())
    for routine in routines:
        routine["_id"] = str(routine["_id"])
    return routines

@recommend.post("/api/skincare-routine/routine_acne/")
async def get_acne_scar_routines(data: recommendMessage):
    recommend_guide = RecommendGuide()
    print(data.messageUser)
    medical_list = []
    acne_counts = {}  # Dictionary để lưu số mụn của từng loại
    total_acne = 0

    acne_treatment = acne_detection_table.find_one({
        "user_id": data.user_id,
    })

    if acne_treatment is not None:
        medical_list = acneDetectionFormat(acne_treatment)
        for medical in medical_list["predicted_images"]:
            if medical["architecture_ai_name"] == "YoloV8 with SAHI":
                total_acne += medical["total_acnes"]
                for result in medical["predicted"]:
                    acne_type = result["class_name"]
                    if acne_type in acne_counts:
                        acne_counts[acne_type] += 1
                    else:
                        acne_counts[acne_type] = 1
        if total_acne == 0:
            answer =  {
                "type": "chat",
                "message": 'No information about acne of user',
                "role": "bot",
                "rag": True,    
                "db": True,
                "recommend": []
            }
            return {"message": "recommend has been created successfully", "chatbox": answer}
        
    sorted_acnes = sorted(acne_counts.items(), key=lambda x: x[1], reverse=True)
    acne_types = [acne[0] for acne in sorted_acnes]

    # Query các routine có acne_treatment là "acne_scar"
    query = {"acne_treatment": {"$in": acne_types}}

    routines = list(skincare_routine_table.find(query))
    print(f"Số lượng routines: {len(routines)}")

    # Chuyển đổi ObjectId thành chuỗi để trả về JSON
    for routine in routines:
        routine["_id"] = str(routine["_id"])
    

    
    # print(routines)
    if len(routines) > 0:
        top_5 = recommend_guide.calculate_cosine_get_top_5(routines, data.messageUser)
        print(top_5)
        length = len(top_5)
        print(f"Số lượng routines: {length}")
        top_like = recommend_guide.calculate_total_likes_get_top(top_5)
        message_guide = ""
        message_guide = recommend_guide.treatment_gpt_acne_detect(treatment_routine=top_like)
        answer =  {
            "user_id":data.user_id, 
            "type": "recommend",
            "message": message_guide,
            "role": "bot",
            "rag": True,    
            "db": True,
            "recommend": top_like
        }
    else:
        answer =  {
                "user_id": data.user_id,
                "type": "chat",
                "message": 'No information about treatment for of user!',
                "role": "bot",
                "rag": True,    
                "db": True,
                "recommend": None
            }
    return {"message": "recommend has been created successfully", "chatbox": answer}

# @recommend.put("/api/skincare-routine/{routine_id}/{product}")
# async def put_skincare_routine_by_id(routine_id: str, product: str):
#     print(product)
#     try:
#         routine = skincare_routine_table.find_one({"_id": ObjectId(routine_id)})
#         if routine is None:
#             raise HTTPException(status_code=404, detail="Skincare routine not found")
#         routine["_id"] = str(routine["_id"])
#         return routine
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Invalid ID format")

@recommend.put("/api/skincare-routine/{routine_id}/{product}")
async def put_skincare_routine_by_id(routine_id: str, product: str):
    try:
        routine = skincare_routine_table.find_one({"_id": ObjectId(routine_id)})
        if routine is None:
            raise HTTPException(status_code=404, detail="Skincare routine not found")
        updated = False
        for item in routine["daily_routine"]["morning"]:
            if item["product"] == product:
                item["like"] = item.get("like", 0) + 1
                updated = True
        for item in routine["daily_routine"]["evening"]:
            if item["product"] == product:
                item["like"] = item.get("like", 0) + 1
                updated = True
        if not updated:
            raise HTTPException(status_code=404, detail="Product not found in routine")
        skincare_routine_table.update_one(
            {"_id": ObjectId(routine_id)},
            {"$set": {"daily_routine": routine["daily_routine"]}}
        )
        routine["_id"] = str(routine["_id"])
        return routine

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")
