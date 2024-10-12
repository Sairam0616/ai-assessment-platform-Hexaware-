# app/models.py
from pydantic import BaseModel, Field
from typing import List, Dict

# Schema for storing candidate responses
class CandidateResponse(BaseModel):
    candidate_id: str = Field(..., description="The unique ID of the candidate (could be email or a user ID)")
    username: str = Field(..., description="The username or email of the candidate")
    exam_title: str = Field(..., description="The title of the exam the candidate is taking")
    responses: Dict[str, str] = Field(..., description="A dictionary mapping question IDs to candidate's responses")
    submitted_at: str = Field(..., description="Timestamp when the exam was submitted")

# Schema for response submission and evaluation
class EvaluationResponse(BaseModel):
    question_id: str = Field(..., description="The ID of the question")
    correct_answer: str = Field(..., description="The correct answer for the question")
    candidate_response: str = Field(..., description="The candidate's answer for the question")
    is_correct: bool = Field(..., description="Whether the candidate's answer is correct or not")
