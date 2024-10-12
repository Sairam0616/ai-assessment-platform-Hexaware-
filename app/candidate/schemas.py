from typing import Optional
from pydantic import BaseModel

class Notifications(BaseModel):
    examReminders: bool
    resultNotifications: bool

class CandidateProfileResponse(BaseModel):
    username: Optional[str] = None
    email: Optional[str] =None
    mobile: Optional[str] = None
    dob: Optional[str] = None
    location: Optional[str] = None

class UpdateCandidateProfile(BaseModel):
    username: Optional[str] = None
    email: Optional[str] =None
    mobile: Optional[str] = None
    dob: Optional[str] = None
    location: Optional[str] = None
