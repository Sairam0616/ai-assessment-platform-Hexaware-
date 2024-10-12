from http import client 
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import httpx
import requests

# Importing existing routers
from app.auth.routes import router as auth_router
from app.admin.routes import router as admin_router
from app.candidate.routes import router as candidate_router
from app.educator.routes import router as educator_router
from app.user.routes import router as user_router  # Importing the new user router
from app.password.routes import router as password_router
from app.exam.routes import router as results_router
from app.proctoring.routes import router as proctoring_router

app = FastAPI()

# Allow origins for CORS (local and production)
origins = ["http://localhost:3000", "http://your-frontend-domain.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers with prefixes
app.include_router(auth_router)
app.include_router(admin_router, tags=["admin"])
app.include_router(candidate_router, tags=["candidate"])
app.include_router(educator_router, tags=["educator"])
app.include_router(user_router, tags=["user"])  # Including the new user management router
app.include_router(password_router, tags=["reset"])
app.include_router(results_router, tags=["results"])
app.include_router(proctoring_router, tags=["proctoring"])

# Hugging Face API details
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-2.7B"
HUGGING_FACE_API_KEY = "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"  # Use your actual key

# Pydantic model for AI suggestions response
class SuggestionsResponse(BaseModel):
    suggestions: List[str]

@app.post("/upload-and-get-suggestions/", response_model=SuggestionsResponse)
async def upload_and_get_suggestions(file: UploadFile = File(...)):
    try:
        # Validate the file type
        if file.content_type != "text/plain":
            raise HTTPException(status_code=400, detail="Only text files are accepted.")

        # Read the file content
        content = await file.read()

        # Decode content to a string
        content_str = content.decode("utf-8")

        # Send the file content to Hugging Face API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                HUGGING_FACE_API_URL,
                headers={"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"},
                json={"inputs": content_str}
            )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        # Extract the generated text from the response
        response_data = response.json()

        # Initialize an empty list for suggestions
        suggestions = []

        # Check if response_data is a list or a dictionary
        if isinstance(response_data, list):
            suggestions = [item['generated_text'] for item in response_data]
        elif isinstance(response_data, dict) and 'generated_text' in response_data:
            suggestions.append(response_data['generated_text'])
        else:
            raise HTTPException(status_code=500, detail="Unexpected response format from the AI model")

        # Split the generated text into separate suggestions
        suggestions = [suggestion.strip() for suggestion in suggestions[0].split('\n') if suggestion.strip()]

        # Return the suggestions
        return SuggestionsResponse(suggestions=suggestions)

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Failed to decode file content. Please upload a valid text file.")
    except httpx.RequestError as req_ex:
        raise HTTPException(status_code=500, detail=f"Error in request to Hugging Face API: {str(req_ex)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")
    
headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
}

class InputText(BaseModel):
    text: str

@app.post("/get-suggestions/")
async def get_suggestions(input_text: InputText):
    try:
        response = requests.post(HUGGING_FACE_API_URL, headers=headers, json={"inputs": input_text.text})
        
        # Log the raw response for debugging
        print("Raw response from Hugging Face API:", response.json())
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
        response_data = response.json()
        
        # Extract the generated text from the response
        if isinstance(response_data, list) and len(response_data) > 0:
            suggestions = response_data[0]["generated_text"].split('\n')  # Split by new line to get separate suggestions
            return {"suggestions": suggestions}
        else:
            return {"suggestions": []}  # Return empty list if no suggestions found

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    


# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Assessment Platform"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}
