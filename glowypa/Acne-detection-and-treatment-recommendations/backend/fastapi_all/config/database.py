from pymongo import MongoClient

client = MongoClient("")

db = client.todo_db

collection_name = db["todo_collection"]
modelai_table = db["modelai_table"]
model_chat = db["model_chat"]
model_acne_treatment = db["model_acne_treatment"]
user_table = db["user_table"]
feedback_table = db["feedback_table"]
architecture_table = db["architecture_table"]
acne_detection_table = db["acne_detection_table"]
skincare_routine_table = db["skincare_routine_table"]
routine_favourit_table= db["routine_favourit_table"]

#
