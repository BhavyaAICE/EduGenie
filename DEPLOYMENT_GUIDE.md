# Frankenstein Web & Deploy: EduGenie Universal Cloud Deployment Guide

This guide provides platform-agnostic instructions for deploying the integrated EduGenie application to modern cloud hosting platforms (such as Render, Railway, Koyeb, Fly.io, or Docker containers) without relying on proprietary platform configuration files.

---

## 1. Universal Deployment Specification

Any standard web service host that supports Python or Docker can host the integrated EduGenie application.

### Standard Service Parameters:
| Setting | Recommended Value | Notes |
|---|---|---|
| **Service Type** | Web Service / HTTP Ingress | Serves both static frontend and API routes |
| **Runtime** | Python 3.10 / 3.11 / 3.12 / 3.13 | |
| **Build Command** | `pip install -r requirements.txt` | Installs runtime dependencies |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}` | Dynamically binds to host-assigned `$PORT` on `0.0.0.0` |
| **Health Check Path**| `/health` | Returns HTTP 200 `{"status": "healthy"}` |
| **Required Secrets**| `GOOGLE_API_KEY` | Gemini API key from Google AI Studio |

---

## 2. Generic Cloud Deployment Steps (Dashboard Configuration)

Whether you choose Render, Railway, Koyeb, or any PaaS:

### Step 1: Push Repaired Code to GitHub
1. Create a repository on your GitHub account (e.g., `edugenie-integrated`).
2. Push your integrated project:
   ```bash
   git init
   git add .
   git commit -m "feat: Integrated EduGenie unified service"
   git branch -M main
   git remote add origin https://github.com/<your-username>/edugenie-integrated.git
   git push -u origin main
   ```

### Step 2: Configure Web Service in Platform Dashboard
1. Create a **New Web Service** and link your GitHub repository.
2. Fill in the build and start configuration:
   - **Environment / Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`
3. Set the Health Check endpoint path to `/health`.

### Step 3: Configure Environment Variables
In the platform's **Environment / Secrets** tab, set:
- `GOOGLE_API_KEY`: `<Your Google Gemini API Key>`
- *(Optional)* `PORT`: If not injected automatically by the platform, default to `8000`.

### Step 4: Deploy & Verify
1. Trigger the deployment.
2. In the build/runtime logs, confirm:
   - Packages from `requirements.txt` install cleanly.
   - Uvicorn server binds to `http://0.0.0.0:<PORT>`.
   - The health check at `/health` passes.
3. Open your assigned public service URL.

---

## 3. Alternative: Containerized Deployment (Dockerfile)

For deployment on Docker-based platforms, self-hosted VPS, AWS ECS, or Fly.io:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install curl for container health check
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Default port fallback
ENV PORT=8000
EXPOSE 8000

# Run uvicorn binding to 0.0.0.0 and dynamic $PORT
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Local Docker Testing:
```bash
docker build -t edugenie-app .
docker run -p 8000:8000 -e GOOGLE_API_KEY="your_api_key_here" edugenie-app
```

---

## 4. Post-Deployment Feature Checklist

Verify all five learning features on your live public URL:
1. **Health Check**: Open `https://<your-app-url>/health` -> Must return HTTP 200 with `{"status": "healthy"}`.
2. **Frontend UI**: Open `https://<your-app-url>/` -> Stylesheet, fonts, and workspace tabs must render cleanly.
3. **QnA Hub**: Ask "What is machine learning?" -> Verifies AI question answering.
4. **Concept Explainer**: Submit "Quantum Entanglement" -> Verifies conceptual breakdown analogies.
5. **Summarizer**: Paste a paragraph and select "short" -> Verifies bullet-point summary generation.
6. **Quiz Engine**: Generate a 3-question quiz on "Python" -> Verifies multiple-choice option rendering and scoring.
7. **Curriculum Roadmap**: Generate a beginner roadmap for "Web Development" -> Verifies multi-phase roadmap timeline.

---

## 5. Common Deployment Pitfalls & Diagnostics

| Symptom | Root Cause | Fix |
|---|---|---|
| **Public URL times out / Refuses connection** | `main.py` binds to `host="127.0.0.1"` (loopback) instead of `host="0.0.0.0"`. | Ensure start command uses `--host 0.0.0.0`. |
| **Port scan timeout** | Server hardcodes static port (e.g. `8000`) instead of reading `$PORT`. | Use `--port ${PORT:-8000}`. |
| **AI requests return 500 / Error** | `GOOGLE_API_KEY` missing in hosting provider environment settings. | Add `GOOGLE_API_KEY` in cloud dashboard secrets. |
| **Frontend assets missing / 404** | Static files not placed in `static/` or mount missing. | Ensure `static/index.html` and `static/style.css` exist. |
