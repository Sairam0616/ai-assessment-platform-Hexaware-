from datetime import datetime
from pydantic import BaseModel, validator, ValidationError
from typing import List, Optional

class RunCaseResponse(BaseModel):
    input: str
    output: str

class QuestionResponse(BaseModel):
    type: str
    question: str
    options: List[str]
    answer: Optional[str] = None  # Mark as Optional
    runCases: List[RunCaseResponse]

class AssessmentResponse(BaseModel):
    title: str
    description: str
    questions: List[QuestionResponse]

class BulkActionResponse(BaseModel):
    message: str  # Simple message confirming the action, e.g., "Archived 3 assessments"
 
class AssessmentSettings(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    webcam: Optional[bool] = False
    microphone: Optional[bool] = False
    screen_sharing: Optional[bool] = False
    selected_assessment: Optional[str] = None 
    
    class Config:
        orm_mode = True

    # Validate that start_time and end_time are valid ISO strings
    @validator('start_time', 'end_time', pre=True)
    def check_datetime_format(cls, v):
        if not isinstance(v, str):
            raise ValueError("Must be a string")
        try:
            # Validate that the value can be converted to a datetime
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("Invalid datetime format, must be ISO format.") 

class AssessmentSettingsResponse(BaseModel):
    assessment_settings: AssessmentSettings
    
class AssessmentStatus(BaseModel):
    title: str
    start_time: datetime  # or datetime, based on your actual data type
    end_time: datetime    # or datetime
    webcam: bool
    microphone: bool
    screen_sharing: bool
    selected_assessment: Optional[str] = None  # Ensure optional fields are marked