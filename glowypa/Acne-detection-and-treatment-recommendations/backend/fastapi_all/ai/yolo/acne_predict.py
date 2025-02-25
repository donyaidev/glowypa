from sahi import AutoDetectionModel
from sahi.utils.cv import read_image
from sahi.utils.file import download_from_url
from sahi.predict import get_prediction, get_sliced_prediction, predict
from sahi.prediction import visualize_object_predictions
from IPython.display import Image
from numpy import asarray
import cv2
import time
import cv2
import numpy as np
from datetime import datetime
import sys
import os
sys.path.append(f'./ai/yolo/ultralytics')
from ultralytics import YOLO
import torch
import base64

# MODEL_PATH = f'{pwd}ai/yolo/weight_acne/best_640img.pt'
MODEL_PATH = f'./ai/yolo/weight_acne/best_aug.pt'

detection_model = AutoDetectionModel.from_pretrained(
    model_type= "yolov8",
    model_path = MODEL_PATH,
    confidence_threshold=0.05,
    device="cuda:0"
)

def acnePredictWithYolo(file_path):
    result = get_prediction(file_path, detection_model)
    detections = result.object_prediction_list 
    boundingbox = []
    for detection in detections:
        bbox = detection.bbox 
        x_min = float(bbox.minx) 
        y_min = float(bbox.miny)  
        x_max = float(bbox.maxx) 
        y_max = float(bbox.maxy)  
        confidence = float(detection.score.value)  
        class_name = detection.category.name 
        boundingbox.append({
            'confidence': confidence,
            'class_name': class_name,
            'x_min': x_min,
            'x_max': x_max,
            'y_max': y_max,
            'y_min': y_min
        })    
    result.export_visuals("./ai/yolo/image_predict")
    return {'message': 'YoloV8', 'bounding-box': boundingbox}

def acnePredictWithSahi(file_path):
    result = get_sliced_prediction(
        file_path,  
        detection_model=detection_model,
        slice_height=258,
        slice_width=258,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0.2
    )
    detections = result.object_prediction_list 
    boundingbox = []
    for detection in detections:
        bbox = detection.bbox 
        x_min = float(bbox.minx)  
        y_min = float(bbox.miny)  
        x_max = float(bbox.maxx) 
        y_max = float(bbox.maxy) 
        confidence = float(detection.score.value)  
        class_name = detection.category.name 
        boundingbox.append({
            'confidence': confidence,
            'class_name': class_name,
            'x_min': x_min,
            'x_max': x_max,
            'y_max': y_max,
            'y_min': y_min
        })    
    result.export_visuals("./ai/yolo/image_predict")
    return {'message': 'YoloV8 with SAHI', 'bounding-box': boundingbox}

