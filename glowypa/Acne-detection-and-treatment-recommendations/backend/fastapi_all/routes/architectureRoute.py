from fastapi import APIRouter, HTTPException
from models.architectureAI_table import ArchitectureAiTable, ArchitectureAiFormat
from config.database import architecture_table
from bson import ObjectId
from schema.schemaArchitecture import architectureFormat, architecturesFormat
from datetime import datetime

architecture = APIRouter()

@architecture.get("/api/architecture/")
async def get_all_architectures():
    architectures = architecture_table.find()
    return architecturesFormat(architectures)

@architecture.post("/api/architecture/")
async def create_architecture(architecture: ArchitectureAiTable):
    data = {
        "ai_name": architecture.ai_name,
        "ai_description": architecture.ai_description,
        "date": datetime.now()
    }
    result = architecture_table.insert_one(data)
    inserted_architecture = architecture_table.find_one({"_id": result.inserted_id})
    return {"message": "Architecture has been created successfully", "architecture": architectureFormat(inserted_architecture)}

@architecture.put("/api/architecture/")
async def update_architecture(architecture: ArchitectureAiFormat):
    architecture_id = ObjectId(architecture.id_architecture)
    architecture_data = architecture_table.find_one({"_id": architecture_id})
    if not architecture_data:
        raise HTTPException(status_code=404, detail="Architecture not found")
    update_data = architecture.dict(exclude_unset=True, exclude={"id_architecture"})
    result = architecture_table.update_one({"_id": architecture_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made to the architecture")
    return {"message": "Architecture has been updated successfully"}


@architecture.delete("/api/architecture/{architecture_id}")
async def delete_architecture(architecture_id: str):
    result = architecture_table.delete_one({"_id": ObjectId(architecture_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Architecture not found")
    return {"message": "Architecture has been deleted successfully"}