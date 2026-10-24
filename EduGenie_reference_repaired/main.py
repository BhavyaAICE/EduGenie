"""
EduGenie - Fully Integrated & Repaired Application Entry Point
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Import all modular routers
from routers.qa_router import router as qa_router
from routers.explanation_router import router as explanation_router
from routers.quiz_router import router as quiz_router
from routers.summary_router import router as summary_router
from routers.learning_router import router as learning_router

# Initialize FastAPI application
app = FastAPI(
    title="EduGenie",
    description="AI-Powered Educational Assistant (Repaired & Fully Integrated)",
    version="1.0.0"
)

# Enable CORS for cross-origin or standalone testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static asset directory
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_frontend():
    """Serve the main single-page application frontend."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend index.html not found in static/"}


# Repaired Health Check Endpoint
@app.get("/health")
def health_check():
    """Service health check endpoint."""
    return {"status": "healthy", "service": "EduGenie", "version": "1.0.0"}


# ─── Registered Routers ─────────────────────────────────────────────
app.include_router(qa_router)
app.include_router(explanation_router)
app.include_router(quiz_router)       # Repaired: Router included
app.include_router(summary_router)
app.include_router(learning_router)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
