from fastapi import APIRouter, HTTPException
from app.candidate.models import Candidate, Notifications, UpdateCandidateProfile
from app.candidate.schemas import UpdateCandidateProfile, CandidateProfileResponse
from typing import Dict
from app.database import candidate_collection  # Ensure your database connection logic is correct

router = APIRouter()

# Get Candidate Dashboard
@router.get("/dashboard")
async def get_candidate_dashboard():
    return {"message": "Candidate Dashboard"}

@router.get("/candidate/profile", response_model=CandidateProfileResponse)
async def get_profile(user_email: str):
    """Fetch candidate profile by email and skip missing fields."""
    # Debugging: Log the email being used to fetch the profile
    print(f"Fetching profile for email: {user_email}")

    # Query the MongoDB to find the candidate by email
    candidate = await candidate_collection.find_one({"email": user_email})

    # If no candidate is found, raise a 404 error
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    # Remove or convert MongoDB _id field
    candidate["_id"] = str(candidate["_id"])

    # Debugging: Log the found candidate profile
    print(f"Found candidate: {candidate}")

    # Prepare the response, checking each field to ensure it exists in the DB
    response_data: Dict[str, str] = {}
    if "username" in candidate:
        response_data["username"] = candidate["username"]
    if "email" in candidate:
        response_data["email"] = candidate["email"]
    if "mobile" in candidate:
        response_data["mobile"] = candidate["mobile"]
    if "dob" in candidate:
        response_data["dob"] = candidate["dob"]
    if "location" in candidate:
        response_data["location"] = candidate["location"]

    # Return the prepared response data using the Pydantic model
    return CandidateProfileResponse(**response_data)


@router.put("/candidate/profile", response_model=CandidateProfileResponse)
async def update_profile(profile_data: UpdateCandidateProfile, user_email: str):
    """Update candidate profile."""
    update_fields = profile_data.dict(exclude_unset=True)  # Only update provided fields

    # Debugging: Log the input email and update fields
    print(f"Updating candidate with email: {user_email}, fields: {update_fields}")

    # Update candidate based on user_email
    result = await candidate_collection.update_one(
        {"email": user_email},
        {"$set": update_fields}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Profile not found or no changes made.")

    # Debugging: Log the updated email after the update
    updated_email = update_fields.get("email", user_email)  # Use the updated email if it's provided
    print(f"Querying candidate with email: {updated_email}")

    # Fetch the updated candidate document from MongoDB
    updated_candidate = await candidate_collection.find_one({"email": updated_email})

    if updated_candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found.")

    # Remove or convert MongoDB _id field
    updated_candidate["_id"] = str(updated_candidate["_id"])

    # Debugging: Log the found candidate
    print(f"Found candidate: {updated_candidate}")

    # Map the MongoDB document to the Pydantic response model
    return CandidateProfileResponse(
        username=updated_candidate["username"],
        email=updated_candidate["email"],
        mobile=updated_candidate["mobile"],
        dob=updated_candidate["dob"],
        location=updated_candidate["location"]
    )


@router.put("/candidate/settings", response_model=Notifications)
async def update_settings(notifications: Notifications, user_email: str):
    """Update candidate settings."""
    result = await candidate_collection.update_one(
        {"email": user_email},
        {"$set": {"notifications": notifications.dict()}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Settings not found or no changes made.")
    
    return notifications

@router.delete("/candidate/delete-account")
async def delete_account(user_email: str):
    """Delete candidate account."""
    result = await candidate_collection.delete_one({"email": user_email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Account not found.")
    
    return {"detail": "Account deleted successfully."}
