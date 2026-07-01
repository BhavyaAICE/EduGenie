"""
EduGenie - Main Application Entry Point

FastAPI application that routes user requests to the appropriate AI module.
Serves the frontend and exposes API endpoints for all educational features.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from qna import get_answer
from explanation_module import get_explanation
from quiz_module import generate_quiz
from summary_module import get_summary
from learning_path import get_learning_path

# Initialize FastAPI app
app = FastAPI(title="EduGenie", description="AI-Powered Educational Assistant")

# Serve static files (HTML, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ─── Request Models ───────────────────────────────────────────────

class QuestionRequest(BaseModel):
    question: str

class ExplanationRequest(BaseModel):
    topic: str

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "Easy"

class SummaryRequest(BaseModel):
    text: str

class LearningPathRequest(BaseModel):
    topic: str
    level: str = "beginner"  # beginner, intermediate, advanced


# ─── Routes ───────────────────────────────────────────────────────

@app.get("/")
async def serve_frontend():
    """Serve the main frontend page."""
    return FileResponse("static/index.html")


@app.post("/qa")
async def question_answer(request: QuestionRequest):
    """Answer an educational question."""
    result = get_answer(request.question)
    return {"response": result}


@app.post("/explain")
async def explain_concept(request: ExplanationRequest):
    """Explain a concept in simple terms."""
    result = get_explanation(request.topic)
    return {"response": result}


@app.post("/quiz")
async def quiz_generation(request: QuizRequest):
    """Generate a quiz on a given topic."""
    result = generate_quiz(request.topic, request.num_questions, request.difficulty)
    return {"response": result}


@app.post("/summarize")
async def summarize_text(request: SummaryRequest):
    """Summarize the provided educational text."""
    result = get_summary(request.text)
    return {"response": result}


@app.post("/learn/recommendations")
async def learning_recommendations(request: LearningPathRequest):
    """Generate a personalized learning path."""
    result = get_learning_path(request.topic, request.level)
    return {"response": result}
