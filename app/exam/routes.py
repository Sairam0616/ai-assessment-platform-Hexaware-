import datetime
from fastapi import APIRouter, HTTPException, Depends
from app.database import assessment_collection, status_collection, results_collection, session_collection
from app.exam.models import CandidateResponse, EvaluationResponse
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Dict, List

# Define the schemas
class PyObjectId(ObjectId):
    """Custom type to handle MongoDB ObjectId in Pydantic models."""
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        schema = handler(core_schema)
        schema.update(type="string")
        return schema

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return handler.generate_schema(str)

class Option(BaseModel):
    text: str

class Question(BaseModel):
    type: str
    question: str
    options: List[Option]
    answer: str

class AssessmentDetail(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # Use alias for consistency
    title: str
    description: str
    questions: List[Question]
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        from_attributes = True

class ExamDetailResponse(BaseModel):
    assessment: AssessmentDetail
    start_time: str
    end_time: str
    webcam: bool
    microphone: bool
    screen_sharing: bool

class Submission(BaseModel):
    email: str
    responses: dict  # {"question_text": "user_answer"}

class Result(BaseModel):
    user_email: str
    assessment_title: str
    total_score: int
    max_score: int
    detailed_results: List[dict]

class Session(BaseModel):
    candidate_email: str
    assessment_title: str
    start_time: datetime.datetime
    end_time: datetime.datetime = None
    completed: bool = False

router = APIRouter()

# Fetch exam details based on the selected assessment from the status_collection
@router.get("/exam/title/{title}", response_model=ExamDetailResponse)
async def get_exam_details(title: str):
    try:
        # Fetch assessment details from the status_collection
        assessment = await status_collection.find_one({"title": title})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # Fetch corresponding questions from the assessment_collection
        questions_data = await assessment_collection.find_one({"title": assessment["selected_assessment"]})
        if not questions_data:
            raise HTTPException(status_code=404, detail="Questions not found for the selected assessment")

        # Prepare the response
        response = {
            "assessment": {
                "id": str(questions_data["_id"]),  # Fetch _id here
                "title": questions_data["title"],
                "description": questions_data["description"],
                "questions": [
                    {
                        "type": question["type"],
                        "question": question["question"],
                        "options": [{"text": option} for option in question["options"]],
                        "answer": question["answer"]
                    }
                    for question in questions_data["questions"]
                ],
                "duration": questions_data.get("duration", 60)  # Add duration field
            },
            "start_time": assessment["start_time"].isoformat(),  # Convert to string
            "end_time": assessment["end_time"].isoformat(),      # Convert to string
            "webcam": assessment["webcam"],
            "microphone": assessment["microphone"],
            "screen_sharing": assessment["screen_sharing"]
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching exam details: {str(e)}")


# Start a new session for the exam
@router.post("/api/candidate/exam/title/{title}/start-session")
async def start_exam_session(title: str, email: str):
    try:
        # Check if the assessment exists
        assessment = await assessment_collection.find_one({"title": title})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # Create a new session
        session_data = {
            "candidate_email": email,
            "assessment_title": title,
            "start_time": datetime.datetime.utcnow(),
            "end_time": None,  # To be set when the exam is submitted
            "completed": False
        }
        result = await session_collection.insert_one(session_data)
        return {"session_id": str(result.inserted_id), "message": "Session started successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting session: {str(e)}")


# Submission API
@router.post("/api/candidate/exam/title/{title}/submit", response_model=Result)
async def submit_exam(title: str, submission: Submission):
    try:
        # Fetch the active session for the candidate
        session = await session_collection.find_one({"candidate_email": submission.email, "assessment_title": title, "completed": False})
        if not session:
            raise HTTPException(status_code=400, detail="No active session found for this candidate.")

        # Fetch the assessment by title
        assessment = await assessment_collection.find_one({"title": title})
        if not assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")

        # Get the questions
        questions = assessment.get("questions", [])
        if not questions:
            raise HTTPException(status_code=404, detail="No questions found for this assessment")

        # Initialize variables for scoring
        total_score = 0
        max_score = len(questions)
        detailed_results = []

        # Iterate through each question and compare answers by the question text or index
        for question in questions:
            question_text = question["question"]
            correct_answer = question["answer"]
            user_answer = submission.responses.get(question_text)

            if user_answer is None:
                # No answer provided for this question
                detailed_results.append({
                    "question": question_text,
                    "correct": False,
                    "user_answer": "No answer",
                    "correct_answer": correct_answer
                })
                continue

            # Check if the answer is correct
            is_correct = user_answer == correct_answer
            if is_correct:
                total_score += 1

            detailed_results.append({
                "question": question_text,
                "correct": is_correct,
                "user_answer": user_answer,
                "correct_answer": correct_answer
            })

        # Create a result entry in the database
        result_data = {
            "user_email": submission.email,
            "assessment_title": title,
            "total_score": total_score,
            "max_score": max_score,
            "detailed_results": detailed_results
        }
        await results_collection.insert_one(result_data)

        # Mark the session as completed and set end time
        await session_collection.update_one({"_id": session["_id"]}, {"$set": {"completed": True, "end_time": datetime.datetime.utcnow()}})

        # Return the result
        return Result(
            user_email=submission.email,
            assessment_title=title,
            total_score=total_score,
            max_score=max_score,
            detailed_results=detailed_results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting exam: {str(e)}")