# EduGenie - AI-Powered Educational Assistant

EduGenie is a lightweight AI-powered educational assistant designed to simplify and enhance the learning experience through the power of Generative AI.

## Features

- **Intelligent Question Answering** (`/qa`)
- **Simplified Concept Explanations** (`/explain`)
- **AI-Powered Quiz Generation** (`/quiz`)
- **Educational Text Summarization** (`/summarize`)
- **Personalized Learning Path Recommendations** (`/learn/recommendations`)

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **AI:** Google Generative AI, Transformers, PyTorch
- **Frontend:** HTML + CSS
- **Validation:** Pydantic
- **Config:** python-dotenv

## Project Structure

```
EduGenie/
├── main.py                  # FastAPI app entry point with all routes
├── qna.py                   # Question Answering module
├── explanation_module.py    # Concept Explanation module
├── quiz_module.py           # Quiz Generation module
├── summary_module.py        # Summarization module
├── learning_path.py         # Learning Path Recommendations module
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore
├── static/
│   ├── index.html           # Frontend UI
│   └── style.css            # Stylesheet
└── README.md
```

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/BhavyaAICE/EduGenie.git
   cd EduGenie
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your Google Generative AI API key to .env
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open in browser**
   ```
   http://127.0.0.1:8000
   ```

## API Endpoints

| Endpoint               | Method | Description                        |
|------------------------|--------|------------------------------------|
| `/qa`                  | POST   | Answer educational questions       |
| `/explain`             | POST   | Explain a concept in simple terms  |
| `/quiz`                | POST   | Generate a quiz on a given topic   |
| `/summarize`           | POST   | Summarize educational text         |
| `/learn/recommendations` | POST | Get personalized learning path     |

## Team

- Built for educational projects and personal learning.
