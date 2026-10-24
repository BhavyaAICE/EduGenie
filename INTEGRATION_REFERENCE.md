# Frankenstein Web & Deploy: EduGenie Integration Reference Guide

This reference guide outlines the target architecture, file integration mapping, import conventions, and execution commands required to reconstruct the unified EduGenie application from the three challenge repositories.

---

## 1. Intended Final Project Structure

```
EduGenie_Integrated/
├── main.py                  # FastAPI application entry point, CORS, routers & static mounts
├── schemas.py               # Pydantic request & response validation schemas
├── requirements.txt         # Consolidated Python dependencies
├── pytest.ini               # Pytest configuration
├── .env.example             # Safe environment variable template
├── .gitignore               # Excludes secrets, caches, and virtualenvs
├── static/
│   ├── index.html           # Single-page application HTML & JS handlers
│   ├── style.css            # Stylesheet (34 KB custom academic aesthetic)
│   └── config.js            # Frontend API configuration (window.API_BASE_URL = "")
├── routers/
│   ├── qa_router.py         # POST /qa
│   ├── explanation_router.py# POST /explain
│   ├── quiz_router.py       # POST /quiz
│   ├── summary_router.py    # POST /summarize
│   └── learning_router.py   # POST /learn/recommendations
├── utils/
│   ├── __init__.py          # Package initializer
│   └── gemini_client.py     # Shared Google GenAI client factory
├── qna.py                   # Domain feature module
├── explanation_module.py    # Domain feature module
├── quiz_module.py           # Domain feature module
├── summary_module.py        # Domain feature module
└── learning_path.py         # Domain feature module
```

---

## 2. File Ownership & Source Mapping

| Target Integrated Path | Origin Repository | Required Modifications During Integration |
|---|---|---|
| `static/index.html` | `frankenstein-edugenie-frontend` | Ensure stylesheet points to `/static/style.css`. Fix Summarizer path to `/summarize`. Fix Curriculum payload to `{ topic, level }`. |
| `static/style.css` | `frankenstein-edugenie-frontend` | None (drop-in). |
| `static/config.js` | `frankenstein-edugenie-frontend` | Set `window.API_BASE_URL = "";` for unified same-origin serving. |
| `main.py` | `frankenstein-edugenie-backend` | Uncomment `app.include_router(quiz_router)`. Update health check route to `@app.get("/health")`. Fix entry point to bind `host="0.0.0.0"` and dynamic `port=int(os.environ.get("PORT", 8000))`. |
| `schemas.py` | `frankenstein-edugenie-backend` | None (drop-in). |
| `routers/explanation_router.py` | `frankenstein-edugenie-backend` | Change response return to `{"response": result}`. |
| `routers/quiz_router.py` | `frankenstein-edugenie-backend` | None (ensure router is included in `main.py`). |
| `routers/qa_router.py` | `frankenstein-edugenie-backend` | None (already canonical). |
| `routers/summary_router.py` | `frankenstein-edugenie-backend` | None (drop-in). |
| `routers/learning_router.py` | `frankenstein-edugenie-backend` | Ensure parameters passed match signature of `learning_path.py`. |
| `qna.py` | `frankenstein-edugenie-features` | None (drop-in). |
| `quiz_module.py` | `frankenstein-edugenie-features` | None (drop-in). |
| `summary_module.py` | `frankenstein-edugenie-features` | None (drop-in). |
| `learning_path.py` | `frankenstein-edugenie-features` | Restore parameter signature to `def get_learning_path(topic: str, level: str = "beginner") -> dict:`. |
| `explanation_module.py` | `frankenstein-edugenie-features` | Ensure `utils` import resolves cleanly via package hierarchy or fallback. |
| `utils/gemini_client.py` | `frankenstein-edugenie-features` | Add `utils/__init__.py`. |

---

## 3. Python Import Strategy

When integrating the modules into the backend service:
1. **Root Module Integration (Recommended)**: Place `qna.py`, `explanation_module.py`, `quiz_module.py`, `summary_module.py`, and `learning_path.py` in the root alongside `main.py`. This mirrors standard Python application layout where `routers/` can import directly via `from qna import get_answer`.
2. **Utils Packaging**: Create `utils/__init__.py` so that `from utils.gemini_client import get_gemini_client` resolves cleanly across both root files and router modules.
3. **Module Isolation (Alternative)**: If participants choose to keep feature code in a `features/` directory, they must either:
   - Add `features` to `sys.path` in `main.py`: `sys.path.insert(0, os.path.join(BASE_DIR, "features"))`
   - Or update imports across all router files to `from features.qna import get_answer`.

---

## 4. Documented API Contract

| Endpoint | Method | Expected Request JSON | Success Response (HTTP 200) | Notes |
|---|---|---|---|---|
| `/` | `GET` | N/A | HTML (`text/html`) | Serves SPA frontend |
| `/static/*` | `GET` | N/A | Static File | Serves CSS and JS assets |
| `/health` | `GET` | N/A | `{"status": "healthy", ...}` | System monitoring |
| `/qa` | `POST` | `{"question": "..."}` | `{"response": "..."}` | Question Answering |
| `/explain` | `POST` | `{"topic": "..."}` | `{"response": "..."}` | Concept Explainer |
| `/quiz` | `POST` | `{"topic": "...", "num_questions": 5, "difficulty": "Easy"}` | `{"response": {"questions": [...]}}` | Quiz Generation |
| `/summarize` | `POST` | `{"text": "...", "length": "medium"}` | `{"response": "..."}` | Text Summarizer |
| `/learn/recommendations` | `POST` | `{"topic": "...", "level": "beginner"}` | `{"response": {"topic": "...", "roadmap": [...]}}` | Curriculum Roadmap |

---

## 5. Consolidated Dependencies Manifest

Create `requirements.txt`:
```
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
google-genai>=2.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
jinja2>=3.1.0
pytest>=8.0.0
httpx>=0.27.0
```

---

## 6. Single Final Application Start Command

### Local Development:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Then visit: `http://127.0.0.1:8000`

### Production / Cloud Deployment:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
