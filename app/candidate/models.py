from pydantic import BaseModel
from typing import Optional, Dict

class Candidate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
   
    mobile: Optional[str] = None
    dob: Optional[str] = None
    location: Optional[str] = None
   # notifications: Dict[str, bool]  # Assuming notifications is a dictionary with string keys and boolean values

class Notifications(BaseModel):
    email_notifications: bool
    sms_notifications: bool

class UpdateCandidateProfile(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    
    mobile: Optional[str] = None
    dob: Optional[str] = None
    location: Optional[str] = None
