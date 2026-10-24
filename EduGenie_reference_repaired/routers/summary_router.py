from fastapi import APIRouter
from schemas import SummaryRequest
from summary_module import get_summary

router = APIRouter()

@router.post("/summarize")
def summarize_text(request: SummaryRequest):
    result = get_summary(request.text, request.length)
    return {"response": result}
