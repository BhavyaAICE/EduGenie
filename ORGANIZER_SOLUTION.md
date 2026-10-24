# Frankenstein Web & Deploy: EduGenie Organizer Solution & Master Repair Manual

> **CONFIDENTIAL — ORGANIZER & EVALUATOR EYES ONLY**  
> Do not distribute or commit this file to any participant-facing repositories.

---

## 1. Executive Summary & Challenge Philosophy

The **Frankenstein Web & Deploy** challenge provides participants with a fragmented, partially broken Python-based educational AI web application split across three Git repositories:
1. `frankenstein-edugenie-frontend` (Repo 1 — Frontend SPA & UI State)
2. `frankenstein-edugenie-backend` (Repo 2 — FastAPI Routing Gateway & Schemas)
3. `frankenstein-edugenie-features` (Repo 3 — AI Generative Modules & Prompting Logic)

The challenge is designed for college and junior-to-mid engineering competitions. It systematically tests:
- Architectural comprehension across decoupled repositories.
- HTTP API contract debugging (CORS, URLs, status codes, JSON payload schemas).
- Python modular packaging, import paths, and dependency manifest migrations.
- Cloud deployment configuration, environment variables, and dynamic port bindings.

---

## 2. Original Architecture Summary

The pristine EduGenie project is a unified Python web application built using **FastAPI**, serving a responsive single-page application (SPA) frontend and integrating with Google Gemini AI models:
- **Framework**: FastAPI + Uvicorn + Jinja2/StaticFiles.
- **Frontend**: HTML5, Vanilla CSS3 (34 KB custom stylesheet), Vanilla ES6 JavaScript.
- **AI Backend**: Google GenAI SDK (`gemini-2.5-flash`), with optional local HuggingFace LaMini fallback.
- **Deployment**: Platform-agnostic cloud / container deployment (Render, Railway, Koyeb, or Docker).

---

## 3. Final Intended Architecture & Integration Topology

The final target architecture is an **Integrated Unified Service**:

```
[Browser Client]
       │
       ▼ (HTTP / Web Requests)
┌─────────────────────────────────────────────────────────────┐
│ EduGenie Unified Service (FastAPI / Uvicorn)               │
│                                                             │
│  ┌─────────────────────────┐  ┌──────────────────────────┐  │
│  │ Static File Mount       │  │ API Routing Layer        │  │
│  │ /static/style.css       │  │ /health                  │  │
│  │ /static/index.html (/)  │  │ /qa                      │  │
│  │ /static/config.js       │  │ /explain                 │  │
│  └─────────────────────────┘  │ /quiz                    │  │
│                               │ /summarize               │  │
│                               │ /learn/recommendations   │  │
│                               └────────────┬─────────────┘  │
│                                            │ (In-Process)   │
│                                            ▼                │
│                               ┌──────────────────────────┐  │
│                               │ Domain Feature Modules   │  │
│                               │ qna.py                   │  │
│                               │ explanation_module.py    │  │
│                               │ quiz_module.py           │  │
│                               │ summary_module.py        │  │
│                               │ learning_path.py         │  │
│                               │ utils/gemini_client.py   │  │
│                               └────────────┬─────────────┘  │
└────────────────────────────────────────────┼────────────────┘
                                             │ (HTTPS API Calls)
                                             ▼
                                  [Google Gemini 2.5 Flash]
```

### Why Unified Service Integration Was Chosen:
- Eliminates unnecessary multi-tier microservice overhead.
- Simplifies free-tier cloud deployment on platforms like Render, Koyeb, or Railway.
- Provides immediate local reproduction with a single `uvicorn main:app --reload` command.

---

## 4. Repository Responsibility & File Ownership Map

| File / Component | Origin Repository | Target Integration Destination | Functional Role |
|---|---|---|---|
| `index.html` | Repo 1 (Frontend) | `static/index.html` | Core UI structure & frontend JavaScript handlers |
| `style.css` | Repo 1 (Frontend) | `static/style.css` | Full application aesthetic stylesheet |
| `config.js` | Repo 1 (Frontend) | `static/config.js` | Configurable API base URL |
| `main.py` | Repo 2 (Backend) | Root `main.py` | FastAPI application instance, CORS, static mounts |
| `schemas.py` | Repo 2 (Backend) | Root `schemas.py` | Pydantic request models & serialization rules |
| `routers/*` | Repo 2 (Backend) | `routers/` | Endpoint route controllers |
| `qna.py` | Repo 3 (Features) | Root `qna.py` (or `features/`) | Question-answering AI engine |
| `explanation_module.py` | Repo 3 (Features) | Root `explanation_module.py` | Concept explanation AI engine |
| `quiz_module.py` | Repo 3 (Features) | Root `quiz_module.py` | Quiz generation AI engine |
| `summary_module.py` | Repo 3 (Features) | Root `summary_module.py` | Educational text summarization engine |
| `learning_path.py` | Repo 3 (Features) | Root `learning_path.py` | Curriculum roadmap synthesizer |
| `utils/gemini_client.py` | Repo 3 (Features) | `utils/gemini_client.py` | Shared Gemini API client initializer |

---

## 5. Complete Inventory of Deliberate Bugs

The challenge incorporates **10 intentional defects** with the targeted difficulty balance:
- **Easy (30%)**: 3 defects
- **Medium (45%)**: 5 defects
- **Hard (25%)**: 2 defects
- **Golden Working Reference**: The `/qa` (QnA Hub) flow is deliberately preserved in full working condition across all three repos to provide participants with an undisputed reference standard.

---

### Bug Detail Table

#### Bug F1 — API Base URL Port Mismatch
- **Difficulty**: Easy (10%)
- **Component**: Repo 1 (Frontend)
- **Exact File**: `config.js`, line 6
- **Buggy Code**:
  ```javascript
  window.API_BASE_URL = "http://localhost:5000";
  ```
- **Why Introduced**: Simulates a common decoupling oversight where frontend developers default to Flask/Node ports (5000) while the backend runs on FastAPI (8000).
- **Observable Symptoms**: Browser DevTools Console shows:
  `GET http://localhost:5000/... net::ERR_CONNECTION_REFUSED`
- **Correct Fix**: Change `config.js` to point to the active backend:
  ```javascript
  // For local development:
  window.API_BASE_URL = "http://127.0.0.1:8000";
  // Or for integrated same-origin deployment:
  window.API_BASE_URL = "";
  ```
- **Acceptable Alternatives**: Hardcoding `""` in `index.html` or passing base URL dynamically via `window.location.origin`.

---

#### Bug F2 — Summarizer Endpoint Path Mismatch
- **Difficulty**: Medium (15%)
- **Component**: Repo 1 (Frontend)
- **Exact File**: `index.html`, line 604
- **Buggy Code**:
  ```javascript
  callAPI('/api/summarize', { text: text, length: currentSummaryLength }, summarizer, summarizerInput, displayQuestion);
  ```
- **Why Introduced**: Tests API contract consistency and endpoint path auditing between frontend calls and registered FastAPI route paths.
- **Observable Symptoms**: Summarizer button returns `HTTP 404 Not Found`.
- **Correct Fix**:
  ```javascript
  callAPI('/summarize', { text: text, length: currentSummaryLength }, summarizer, summarizerInput, displayQuestion);
  ```
- **Acceptable Alternatives**: Adding `@router.post("/api/summarize")` alias on the backend.

---

#### Bug F3 — Curriculum Request Payload Key Mismatch
- **Difficulty**: Medium (15%)
- **Component**: Repo 1 (Frontend)
- **Exact File**: `index.html`, lines 787–790
- **Buggy Code**:
  ```javascript
  body: JSON.stringify({ subject: topic, difficulty_level: level })
  ```
- **Why Introduced**: Tests participant ability to inspect Pydantic validation errors in HTTP responses and correlate frontend JSON bodies with backend schemas.
- **Observable Symptoms**: Browser receives `HTTP 422 Unprocessable Entity`:
  `{"detail":[{"loc":["body","topic"],"msg":"Field required"},{"loc":["body","level"],"msg":"Field required"}]}`
- **Correct Fix**:
  ```javascript
  body: JSON.stringify({ topic: topic, level: level })
  ```

---

#### Bug B1 — Non-Standard Health Check Route
- **Difficulty**: Easy (10%)
- **Component**: Repo 2 (Backend)
- **Exact File**: `main.py`, line 58
- **Buggy Code**:
  ```python
  @app.get("/healthz")
  def health_check():
  ```
- **Why Introduced**: Tests standard API conventions for monitoring endpoints.
- **Observable Symptoms**: Calling `GET /health` returns `404 Not Found`.
- **Correct Fix**:
  ```python
  @app.get("/health")
  def health_check():
  ```
- **Acceptable Alternatives**: Registering both `/health` and `/healthz`.

---

#### Bug B2 — Omitted Quiz Router Inclusion
- **Difficulty**: Medium (15%)
- **Component**: Repo 2 (Backend)
- **Exact File**: `main.py`, line 70
- **Buggy Code**:
  ```python
  # Bug B2 (Intentional): Quiz router registration omitted
  # app.include_router(quiz_router)
  ```
- **Why Introduced**: Tests modular FastAPI router registration.
- **Observable Symptoms**: `POST /quiz` returns `404 Not Found` even though `routers/quiz_router.py` exists and is implemented.
- **Correct Fix**: Uncomment in `main.py`:
  ```python
  app.include_router(quiz_router)
  ```

---

#### Bug B3 — Explanation Response Serialization Key Mismatch
- **Difficulty**: Medium (15%)
- **Component**: Repo 2 (Backend)
- **Exact File**: `routers/explanation_router.py`, line 28
- **Buggy Code**:
  ```python
  return {"explanation": result}
  ```
- **Why Introduced**: Tests frontend-backend contract symmetry. `index.html` helper `addToChatFeed` expects `data.response`.
- **Observable Symptoms**: The concept explanation completes successfully with `200 OK`, but the chat feed displays `undefined`.
- **Correct Fix**:
  ```python
  return {"response": result}
  ```
- **Acceptable Alternatives**: Modifying the frontend `addToChatFeed(section, question, data.response || data.explanation)`.

---

#### Bug B4 — Loopback Host & Hardcoded Port in Deployment Entry Point
- **Difficulty**: Hard (12.5%)
- **Component**: Repo 2 (Backend)
- **Exact File**: `main.py`, lines 74–78
- **Buggy Code**:
  ```python
  if __name__ == "__main__":
      import uvicorn
      uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
  ```
- **Why Introduced**: Classic production deployment failure. Binding to `127.0.0.1` (loopback interface) works when tested locally on the developer's laptop, but in any containerized or cloud environment (Render, Railway, Koyeb, Docker), it rejects all external incoming traffic from ingress proxies and load balancers. Furthermore, hardcoding port 8000 ignores the dynamic `$PORT` environment variable assigned by cloud hosting platforms.
- **Observable Symptoms**: Locally the server starts, but when deployed or run in a container, the public URL times out, returns `502 Bad Gateway`, or fails cloud health checks.
- **Correct Fix**:
  ```python
  if __name__ == "__main__":
      import uvicorn
      port = int(os.environ.get("PORT", 8000))
      uvicorn.run("main:app", host="0.0.0.0", port=port)
  ```
  And for deployment start command: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`.

---

#### Bug M1 — Legacy SDK Package in Requirements
- **Difficulty**: Easy (10%)
- **Component**: Repo 3 (Features)
- **Exact File**: `requirements.txt`, line 3
- **Buggy Code**:
  ```
  google-generativeai==0.8.3
  ```
- **Why Introduced**: Modern Gemini 2.5 Flash code uses `from google import genai` (`google-genai` library), whereas `google-generativeai` is the deprecated legacy library.
- **Observable Symptoms**: Running feature tests or application throws:
  `ModuleNotFoundError: No module named 'google.genai'` or `ImportError: cannot import name 'genai' from 'google'`.
- **Correct Fix**: Replace in `requirements.txt`:
  ```
  google-genai>=2.0.0
  ```

---

#### Bug M2 — Inverted Parameter Order in Learning Path Signature
- **Difficulty**: Medium (15%)
- **Component**: Repo 3 (Features)
- **Exact File**: `learning_path.py`, line 21
- **Buggy Code**:
  ```python
  def get_learning_path(level: str, topic: str) -> dict:
  ```
- **Why Introduced**: Backend calls `get_learning_path(request.topic, request.level)`. Because positional arguments are swapped, `topic` receives `"beginner"` and `level` receives `"Quantum Physics"`, resulting in nonsensical AI prompts or validation errors.
- **Observable Symptoms**: The generated curriculum shows topic as "beginner" and level as "Quantum Physics".
- **Correct Fix**: Restore canonical signature:
  ```python
  def get_learning_path(topic: str, level: str = "beginner") -> dict:
  ```
- **Acceptable Alternatives**: Calling via keyword arguments in `routers/learning_router.py`: `get_learning_path(topic=request.topic, level=request.level)`.

---

#### Bug M3 — Cross-Module Package Import Inconsistency
- **Difficulty**: Hard (12.5%)
- **Component**: Repo 3 (Features)
- **Exact File**: `explanation_module.py`, line 9
- **Buggy Code**:
  ```python
  from utils.gemini_client import get_gemini_client
  ```
- **Why Introduced**: When Repo 3 is integrated into the backend or a subdirectory without proper `sys.path` or package `__init__.py`, Python fails to locate `utils`.
- **Observable Symptoms**: `ModuleNotFoundError: No module named 'utils'`.
- **Correct Fix**: Ensure `utils/__init__.py` exists and fallback imports are present:
  ```python
  try:
      from utils.gemini_client import get_gemini_client
  except ImportError:
      from features.utils.gemini_client import get_gemini_client
  ```

---

## 6. Golden Reference Working Interaction

To ensure the challenge is fair, the **QnA Hub** (`POST /qa`) interaction is kept **100% working and unbugged**:
1. **Frontend**: Calls `${API_BASE_URL}/qa` with payload `{"question": question}`.
2. **Backend**: Routes to `routers/qa_router.py`, validates via `QuestionRequest(question=str)`, calls `get_answer(request.question)`.
3. **Features**: `qna.py` provides `get_answer(question: str) -> str`.
4. **Response**: Returns `{"response": result}` which frontend immediately displays in chat feed.

Participants can use `/qa` as their benchmark to verify connectivity, payload schemas, and response patterns.

---

## 7. Unified Repaired Project Directory Structure

```
EduGenie_Repaired/
├── main.py                  # Entry point with static mounts and all 5 routers
├── schemas.py               # Pydantic schemas
├── requirements.txt         # Consolidated dependencies
├── pytest.ini               # Pytest configuration
├── .env.example             # Safe environment template
├── .gitignore               # Clean git exclusions
├── static/
│   ├── index.html           # SPA template with repaired API calls
│   ├── style.css            # Stylesheet
│   └── config.js            # window.API_BASE_URL = ""
├── routers/
│   ├── qa_router.py         # /qa
│   ├── explanation_router.py# /explain (returning "response")
│   ├── quiz_router.py       # /quiz (registered in main.py)
│   ├── summary_router.py    # /summarize
│   └── learning_router.py   # /learn/recommendations
├── utils/
│   ├── __init__.py
│   └── gemini_client.py     # Centralized Gemini client
├── qna.py                   # Feature module
├── explanation_module.py    # Feature module
├── quiz_module.py           # Feature module
├── summary_module.py        # Feature module
├── learning_path.py         # Feature module (topic, level)
└── tests/
    └── test_integration.py  # 9-point end-to-end integration test suite
```

---

## 8. Consolidated Dependency Requirements

`requirements.txt`:
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

## 9. Evaluation & Scoring Rubric (100 Points Total)

| Category | Evaluation Criteria | Max Points |
|---|---|---|
| **1. Architecture & Integration (25 pts)** | Successfully unified three repositories into a coherent project structure. | 10 |
| | Clean Python packaging with proper imports and `__init__.py`. | 8 |
| | Consolidated, clean `requirements.txt` with correct `google-genai` SDK. | 7 |
| **2. Backend & API Debugging (30 pts)** | Enabled all 5 API routes (fixed `/quiz` router registration). | 8 |
| | Resolved explanation response serialization mismatch (`response` vs `explanation`). | 8 |
| | Corrected health check endpoint to `/health`. | 4 |
| | Configured CORS middleware properly for browser access. | 5 |
| | Corrected parameter order in `learning_path.py`. | 5 |
| **3. Frontend UI Integration (20 pts)** | Resolved API base URL configuration in `config.js`. | 6 |
| | Fixed Summarizer endpoint path mismatch (`/summarize`). | 7 |
| | Corrected Curriculum request payload keys (`topic`, `level`). | 7 |
| **4. Cloud Deployment & Live Demo (25 pts)** | Fixed production host (`0.0.0.0`) and dynamic `$PORT` binding in entry point. | 10 |
| | Deployed to publicly accessible URL (Render, Koyeb, Railway, etc.). | 10 |
| | Live demonstration of all 5 functional learning tools with Gemini AI. | 5 |
| **Total** | | **100 Points** |

---

## 10. Organizer Verification Status

A pristine reference implementation has been built and validated at `c:\Users\Bhavy\Desktop\EduGenie\EduGenie_reference_repaired`.

### Automated Verification Results:
```
============================= test session starts =============================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Bhavy\Desktop\EduGenie\EduGenie_reference_repaired
configfile: pytest.ini
collected 9 items

tests\test_integration.py .........                                      [100%]

============================= 9 passed in 49.00s ==============================
```
All 9 automated integration tests passed with 100% success rate.
