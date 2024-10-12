# app/educator/routes.py
from datetime import datetime
from typing import List, Optional
from wsgiref.validate import validator
from app.educator.schemas import AssessmentResponse, AssessmentSettingsResponse, AssessmentStatus, QuestionResponse, RunCaseResponse
from fastapi import APIRouter, HTTPException, Query, Body
from app.database import assessment_collection, status_collection
from app.educator.models import BulkActionRequest
from app.educator.schemas import BulkActionResponse
from app.educator.schemas import AssessmentSettings
from app.educator.models import Assessment

router = APIRouter()

@router.post("/auth/assessments")
async def create_assessment(assessment: Assessment):
    # Create assessment document
    assessment_data = assessment.dict()
    # Add educator_email from the assessment model
    educator_email = assessment_data.pop("educator_email")
    print(f"educator:{educator_email}")
    # Save the assessment to the database
    assessment_data["educator_email"] = educator_email
    result = await assessment_collection.insert_one(assessment_data)

    if result.inserted_id:
        return {"message": "Assessment created successfully!", "assessment_id": str(result.inserted_id)}
    raise HTTPException(status_code=400, detail="Failed to create assessment")


@router.get("/auth/assessments", response_model=List[AssessmentResponse])
async def get_assessments(title: str = Query(None)):
    query = {"title": {"$regex": title, "$options": "i"}} if title else {}
    assessments = []

    async for assessment in assessment_collection.find(query):
        # Construct the response object using the existing schema
        assessment_response = AssessmentResponse(
            title=assessment.get("title"),
            description=assessment.get("description"),
            questions=[
                QuestionResponse(
                    type=question["type"],
                    question=question["question"],
                    options=question.get("options", []),
                    # Handle cases where answer might be None
                    answer=question.get("answer") or "",  # Default to an empty string
                    runCases=[
                        RunCaseResponse(input=run_case["input"], output=run_case["output"])
                        for run_case in question.get("runCases", [])
                    ],
                ) for question in assessment.get("questions", [])
            ]
        )
        assessments.append(assessment_response)

    if not assessments:
        raise HTTPException(status_code=404, detail="No assessments found")

    return assessments

# Bulk delete assessments
@router.post("/auth/assessments/bulk-delete", response_model=BulkActionResponse)
async def bulk_delete_assessments(request: BulkActionRequest):
    # Delete multiple assessments by title
    delete_result = await assessment_collection.delete_many({"title": {"$in": request.titles}})

    if delete_result.deleted_count > 0:
        return BulkActionResponse(message=f"Deleted {delete_result.deleted_count} assessments successfully.")
    raise HTTPException(status_code=404, detail="No assessments found to delete.")

# Bulk archive assessments
@router.post("/auth/assessments/bulk-archive", response_model=BulkActionResponse)
async def bulk_archive_assessments(request: BulkActionRequest):
    # Archive assessments by setting a status field to 'Archived'
    update_result = await assessment_collection.update_many(
        {"title": {"$in": request.titles}},
        {"$set": {"status": "Archived"}}
    )

    if update_result.modified_count > 0:
        return BulkActionResponse(message=f"Archived {update_result.modified_count} assessments successfully.")
    raise HTTPException(status_code=404, detail="No assessments found to archive.")



@router.post("/auth/assessments/settings")
async def save_or_update_assessment_settings(settings: AssessmentSettings):
    # Validate fields
    if not settings.title:
        raise HTTPException(status_code=400, detail="Title is required.")

    # Ensure start_time is before end_time
    if settings.start_time >= settings.end_time:
        raise HTTPException(status_code=400, detail="Start time must be before end time.")

    # Check if the assessment exists in the assessment collection
    existing_assessment = await assessment_collection.find_one({"title": settings.title})
    if not existing_assessment:
        raise HTTPException(status_code=404, detail=f"Assessment '{settings.title}' not found in assessment db.")

    # Check if the settings for this assessment already exist in the status collection
    existing_settings = await status_collection.find_one({"title": settings.title})

    setting_data = settings.dict()

    if existing_settings:
        # Update the existing settings document
        result = await status_collection.update_one(
            {"_id": existing_settings["_id"]},
            {"$set": setting_data}
        )
        if result.modified_count == 1:
            return {"message": "Assessment settings updated successfully!", "updated_id": str(existing_settings["_id"])}
        else:
            raise HTTPException(status_code=400, detail="Failed to update settings.")
    else:
        # Insert a new settings document
        result = await status_collection.insert_one(setting_data)
        if not result.inserted_id:
            raise HTTPException(status_code=400, detail="Failed to save settings.")
        return {"message": "Assessment settings saved successfully!", "saved_id": str(result.inserted_id)}



@router.get("/auth/assessments/settings/{title}", response_model=AssessmentSettingsResponse)
async def get_assessment_settings(title: str):
    settings = await status_collection.find_one({"title": title})
    if not settings:
        raise HTTPException(status_code=404, detail=f"Settings for assessment '{title}' not found.")

    # Convert datetime objects to ISO 8601 strings
    if isinstance(settings.get("start_time"), datetime):
        settings["start_time"] = settings["start_time"].isoformat()
    if isinstance(settings.get("end_time"), datetime):
        settings["end_time"] = settings["end_time"].isoformat()

    return {"assessment_settings": settings}


@router.get("/auth/assessments/status", response_model=List[AssessmentStatus])
async def get_assessment_settings(title: str = Query(None)):
    query = {"title": {"$regex": title, "$options": "i"}} if title else {}
    settings_list = []

    async for settings in status_collection.find(query):
        print(settings)  # Debugging output to check fetched data
        settings_response = AssessmentStatus(
            title=settings.get("title"),
            start_time=settings.get("start_time"),  # Assume these are datetime objects
            end_time=settings.get("end_time"),      # Assume these are datetime objects
            webcam=settings.get("webcam"),
            microphone=settings.get("microphone"),
            screen_sharing=settings.get("screen_sharing"),
            selected_assessment=settings.get("selected_assessment")  # Optional field
        )
        settings_list.append(settings_response)

    if not settings_list:
        raise HTTPException(status_code=404, detail="No settings found for the specified assessments")

    return settings_list
