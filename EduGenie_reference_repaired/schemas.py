"""
EduGenie Backend Request and Response Schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class QuestionRequest(BaseModel):
    question: str = Field(..., description="The student's question")


class ExplanationRequest(BaseModel):
    topic: str = Field(..., description="Academic concept or topic to explain")


class QuizRequest(BaseModel):
    topic: str = Field(..., description="Topic of the quiz")
    num_questions: int = Field(default=5, ge=1, le=10, description="Number of questions (1-10)")
    difficulty: str = Field(default="Easy", description="Difficulty level: Easy, Medium, Hard")


class SummaryRequest(BaseModel):
    text: str = Field(..., description="Educational text to summarize")
    length: str = Field(default="medium", description="Summary depth: short, medium, detailed")


class LearningPathRequest(BaseModel):
    topic: str = Field(..., description="Curriculum subject or discipline")
    level: str = Field(default="beginner", description="Proficiency level: beginner, intermediate, advanced")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
