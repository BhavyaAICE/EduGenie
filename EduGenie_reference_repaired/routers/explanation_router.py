from fastapi import APIRouter
from schemas import ExplanationRequest
from explanation_module import get_explanation

router = APIRouter()

@router.post("/explain")
def explain_concept(request: ExplanationRequest):
    result = get_explanation(request.topic)
    # Repaired: Frontend expects property key 'response'
    return {"response": result}
