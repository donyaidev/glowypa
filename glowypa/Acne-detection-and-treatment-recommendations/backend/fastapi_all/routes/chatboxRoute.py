from fastapi import APIRouter, HTTPException
from config.database import architecture_table
from bson import ObjectId
from schema.schemaArchitecture import architectureFormat, architecturesFormat
from datetime import datetime
# from ai.rag.ragWithDocs import mainChat
# from ai.rag.rag_llma import mainChat
from models.chatbox_table import ChatboxMessage
from config.database import acne_detection_table
from schema.schemaAcneDetection import acneDetectionFormat
from treatment.treatment_main import TreatmentChat

import os
import re

chatbox = APIRouter()

def remove_html_tags(text):
    clean_text = re.sub(r'<.*?>', '', text)
    return clean_text


@chatbox.post("/api/chatbox/")
async def create_chatbox(data: ChatboxMessage):
    advice_treatment = TreatmentChat()
    question = data.message
    chatHistoryCache = []
    chatHistoryList = data.history_chat
    medical_db  = ""
    
    for chatHistory in chatHistoryList:
        chatHistoryCache.append(remove_html_tags(chatHistory["message"]))
    if data.db == True:
        medical_list = []
        medical_acne = set()
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
                        medical_acne.add(result["class_name"])
        medical_db = (
            "Có tổng số lượng đốt mụn là: " + str(total_acne) + "\n"
            + "Các loại mụn đang bị là: " + ", ".join(medical_acne) + "\n"
        )
                 
    response = advice_treatment.advice_treatment_chat(question, chatHistoryCache,medical_db)
    answer = {
        "type": "chat",
        "message": response["message"],
        "role": "bot",
        "rag": data.rag,
        "db": data.db,
        "reference_doc": response["doc_reference"],
        "question_related_acne_medical": response["question_related_acne_medical"]
    }
    return {"message": "Chatbox has been created successfully", "chatbox": answer}


@chatbox.post("/api/chatbox_ance/")
async def create_chatbox(data: ChatboxMessage):
    advice_treatment = TreatmentChat()
    data.db = True
    question = "Bệnh nhân đang bị các loại mụn như trong medical record, hãy đưa ra lời khuyên và cách chữa  trị"
    chatHistoryCache = []
    chatHistoryList = data.history_chat
    medical_db  = ""
    
    for chatHistory in chatHistoryList:
        chatHistoryCache.append(remove_html_tags(chatHistory["message"]))
    if data.db == True:
        medical_list = []
        medical_acne = set()
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
                        medical_acne.add(result["class_name"])
        medical_db = (
            "Có tổng số lượng đốt mụn là: " + str(total_acne) + "\n"
            + "Các loại mụn đang bị là: " + ", ".join(medical_acne) + "\n"
        )
                 
    response = advice_treatment.advice_treatment_chat_acne_detect(question, chatHistoryCache,medical_db)
    answer = {
        "type": "chat",
        "message": response["message"],
        "role": "bot",
        "rag": True,
        "db": True,
        "reference_doc": response["doc_reference"],
        "question_related_acne_medical": response["question_related_acne_medical"]
    }
    return {"message": "Chatbox has been created successfully", "chatbox": answer}



@chatbox.post("/api/recommend_product/")
async def recommend_product(data: ChatboxMessage):
    
    medical_list = []
    medical_acne = set()
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
                    medical_acne.add(result["class_name"])
        if total_acne == 0:
            answer =  {
                "type": "chat",
                "message": 'No information about acne of user',
                "role": "bot",
                "rag": True,    
                "db": True,
            }
            return {"message": "recommend has been created successfully", "chatbox": answer}
    medical_db = (
        "Có tổng số lượng đốt mụn là: " + str(total_acne) + "\n"
        + "Các loại mụn đang bị là: " + ", ".join(medical_acne) + "\n"
    )
        
    import time
    time.sleep(5)
    answer =  {
        "type": "recommend",
        "message": '123',
        "role": "bot",
        "rag": True,    
        "db": True,
        "recommend": {
            "context": "",
            "acne_treatment": "acne_scars",
            "daily_routine": {
            "morning": [
            {
                "step": "Cleanser",
                "product": "Sanctuary Spa's Triple Cleansing Mousse",
                "usage": "Use to cleanse your face.",
                "link": "https://shopee.vn/-Date-9-21-Mousse-r%E1%BB%ADa-m%E1%BA%B7t-tr%E1%BA%AFng-da-AHA-Sanctuary-Spa-Triple-Cleansing-Mousse-150ml-i.1127550.7073380259",
                "image": "https://www.dropbox.com/scl/fi/rvpds2lhoge17xguzx5j3/cleanser.jpg?rlkey=mfkiz3m3otwva5i37qytxgxa4&st=5bivyeoa&dl=1",
                "like": 999,
            },
            {
                "step": "Exfoliator (1-2 times a week)",
                "product": "The Ordinary's Lactic Acid 10% + HA Serum",
                "usage":
                "Use after cleansing, but only in the morning if not microneedling that day. If microneedling, use in the evening.",
                "link": "https://shopee.vn/Tinh-ch%E1%BA%A5t-The-Ordinary-Lactic-Acid-5-10-HA-c%E1%BA%A5p-n%C6%B0%E1%BB%9Bc-s%C3%A1ng-m%E1%BB%8Bn-da-(Bill-Canada-US)-Cila-House-i.249374.1296069913?sp_atk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3&xptdk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3",
                "image": "https://www.dropbox.com/scl/fi/41z1lrh7mozhdyvr93jgr/cream-day.jpg?rlkey=3l5lrbzyu3js5ghod1m2nvtjv&st=g3kpk5qo&dl=1",
                "like": 999,

            },
            {
                "step": "Serum",
                "product": "Pixi Collagen and Retinol Serum",
                "usage": "Apply after exfoliating or after cleansing.",
                "link": "https://www.pixibeauty.com/products/collagen-retinol-serum?srsltid=AfmBOoq_B-2c7Urqjh2WTsih6-Zi_-Ug8QOpDyvXYAk42mqsD4pDwdpg",
                "image": "https://www.dropbox.com/scl/fi/e7h7olov88w7ompyqsh0p/serum.jpg?rlkey=2w2pt2tfhmz6v1gu03yvzchac&st=am9qsd69&dl=1",
                "like": 999,
            },
            {
                "step": "Day Moisturizer",
                "product": "Nivea's Oil Free Face Cream",
                "usage": "Use to keep your skin hydrated.",
                "link": "https://www.amazon.de/-/en/Nivea-Visage-Oil-Free-Face-Milk/dp/B001RYSGEA",
                "image": "https://www.dropbox.com/scl/fi/41z1lrh7mozhdyvr93jgr/cream-day.jpg?rlkey=3l5lrbzyu3js5ghod1m2nvtjv&st=cp5rze7e&dl=1",
                "like": 999,
            },
            {
                "step": "Sunscreen",
                "product": "Skin Defence SPF 50++",
                "usage":"Essential to use in the morning to protect your skin from UV damage.",
                "link": "https://www.thebodyshop.com.vn/kem-chong-nang-skin-defence-multi-protection-light-essence-60ml.html",
                "image": "https://www.dropbox.com/scl/fi/t3ne18inbphk1efq8p1wm/sunscreen.jpg?rlkey=x15f2kjatct6vix0g4zr3btu4&st=o8guq384&dl=1",
                "like": 999,
            },
            ],
            "evening": [
            {
                "step": "Cleanser",
                "product": "Sanctuary Spa's Triple Cleansing Mousse",
                "usage": "Cleanse your face before bed.",
                "link": "https://shopee.vn/-Date-9-21-Mousse-r%E1%BB%ADa-m%E1%BA%B7t-tr%E1%BA%AFng-da-AHA-Sanctuary-Spa-Triple-Cleansing-Mousse-150ml-i.1127550.7073380259",
                "image": "https://www.dropbox.com/scl/fi/6xx4vyukfeh4asm9qnuyu/celtafill.png?rlkey=mhn98m9ganau9czojax3p8cxl&st=ctklg0h5&dl=1",
                "like": 999,
            },
            {
                "step": "Exfoliator (1-2 times a week)",
                "product": "The Ordinary's Lactic Acid 10% + HA Serum",
                "usage": "Use as mentioned above.",
                "link": "https://shopee.vn/Tinh-ch%E1%BA%A5t-The-Ordinary-Lactic-Acid-5-10-HA-c%E1%BA%A5p-n%C6%B0%E1%BB%9Bc-s%C3%A1ng-m%E1%BB%8Bn-da-(Bill-Canada-US)-Cila-House-i.249374.1296069913?sp_atk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3&xptdk=f94c5d1d-a900-462c-80ff-a8c7cd7b4ec3",
                "image": "https://www.dropbox.com/scl/fi/hv7xibg01q4nvm0md08xn/exfoliator.png?rlkey=yrsq1bzqzvspsqo6qs2hedmr6&st=8ylo37kr&dl=1",
                "like": 999,
            },
            {
                "step": "Serum",
                "product": "Pixi Collagen and Retinol Serum",
                "usage": "Apply after exfoliating.",
                "link": "https://www.pixibeauty.com/products/collagen-retinol-serum?srsltid=AfmBOoq_B-2c7Urqjh2WTsih6-Zi_-Ug8QOpDyvXYAk42mqsD4pDwdpg",
                "image": "https://www.dropbox.com/scl/fi/e7h7olov88w7ompyqsh0p/serum.jpg?rlkey=2w2pt2tfhmz6v1gu03yvzchac&st=fejizr2l&dl=1",
                "like": 999,
            },
            {
                "step": "Night Moisturizer",
                "product": "CeraVe Moisturizing Cream",
                "usage": "Hydrate and restore your skin overnight.",
                "link": "https://shopee.vn/Kem-D%C6%B0%E1%BB%A1ng-%E1%BA%A8m-D%C3%A0nh-Cho-Da-Kh%C3%B4-Cerave-454G-i.152872415.18854062290?sp_atk=c594f888-9457-4708-b1c3-e7a008b3cbc7&xptdk=c594f888-9457-4708-b1c3-e7a008b3cbc7",
                "image": "https://www.dropbox.com/scl/fi/2k2k992r4oys0j6obdis9/cream-night.jpg?rlkey=n6cx0lm41km6ubfnshc67c6ci&st=yj1dax26&dl=1",
                "like": 999,
            },
            ],
            "microneedling": {
            "description":
                "Perform Microneedling: Should be done in the evening, after cleansing and before applying serum and moisturizer. After microneedling, let your skin rest and only use a gentle moisturizer.",
            },
            "notes": [
            "When microneedling, avoid using products containing acids or retinol immediately afterward to prevent skin irritation.",
            "Ensure your skin is well protected during the day, especially after microneedling.",
            ],
      },
    },
    }
    return {"message": "recommend has been created successfully", "chatbox": answer}
