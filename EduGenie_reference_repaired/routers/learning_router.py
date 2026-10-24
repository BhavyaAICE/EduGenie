from fastapi import APIRouter
from schemas import LearningPathRequest
from learning_path import get_learning_path

router = APIRouter()

@router.post("/learn/recommendations")
def learning_recommendations(request: LearningPathRequest):
    result = get_learning_path(request.topic, request.level)
    return {"response": result}
