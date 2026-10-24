from fastapi import APIRouter
from schemas import QuestionRequest
from qna import get_answer

router = APIRouter()

@router.post("/qa")
def question_answer(request: QuestionRequest):
    result = get_answer(request.question)
    return {"response": result}
