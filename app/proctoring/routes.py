from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import asyncio  # Ensure to import asyncio

router = APIRouter()

class ProctoringRequest(BaseModel):
    title: str

@router.post("/api/proctoring/init")
async def initialize_proctoring(request: ProctoringRequest):
    try:
        print(f"Proctoring initialized for title: {request.title}")

        # Simulate some processing time
        await asyncio.sleep(2)

        return {"message": "AI proctoring initialized successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to initialize proctoring.")
