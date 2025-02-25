from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class ImageBase64AndModel(BaseModel):
    image_id: str
    image_base64: str
    
class DeleteAndAddBase64Img(BaseModel):
    img_id_remove_list: List[str]
    image_base64_list: List[ImageBase64AndModel]

class Image(BaseModel):
    image_id: str
    image_base64: str
    
class PredictedImage(BaseModel):
    image_id: str
    predicted: List[Dict[str, float]]
    architecture_ai_name: str
    total_acnes: int
    
class AcneTreatment(BaseModel):
    user_id: str
    images: List[Image]
    date: datetime
    predicted_images: List[PredictedImage]
    