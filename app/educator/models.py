# app/educator/models.py
from pydantic import BaseModel
from typing import List, Optional

class RunCase(BaseModel):
    input: str
    output: str

class Question(BaseModel):
    type: str  # 'multiple-choice', 'short-answer', 'coding-challenge'
    question: str
    options: Optional[List[str]] = []
    answer: Optional[str] = None
    runCases: Optional[List[RunCase]] = []

class Assessment(BaseModel):
    title: str
    description: str
    questions: List[Question]
    educator_email: str  # Field to map the educator's email
    
class BulkActionRequest(BaseModel):
    titles: List[str]  # List of titles for bulk actions

# Optional: if you plan to use IDs instead, you can change titles to IDs
# class BulkActionRequest(BaseModel):
#     ids: List[str]  # List of IDs for bulk actions    