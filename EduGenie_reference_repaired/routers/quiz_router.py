from fastapi import APIRouter
from schemas import QuizRequest
from quiz_module import generate_quiz

router = APIRouter()

@router.post("/quiz")
def quiz_generation(request: QuizRequest):
    result = generate_quiz(request.topic, request.num_questions, request.difficulty)
    return {"response": result}
