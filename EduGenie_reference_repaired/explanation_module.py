"""
EduGenie Concept Explanation Module (Repaired)
"""

import os
import functools
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Centralized client helper with fallback
try:
    from utils.gemini_client import get_gemini_client
    client = get_gemini_client()
except Exception:
    api_key = os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key) if api_key else None


def _explain_with_gemini(topic: str) -> str:
    """Fallback generator using Google Gemini API."""
    if not client:
        return "Gemini API key is missing. Please set GOOGLE_API_KEY in your environment."

    prompt = f"""You are a friendly teacher. Explain the following topic in very simple, 
    easy-to-understand terms for a student. Use analogies and examples where helpful.
    
    Topic: {topic}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            temperature=0.7
        )
    )
    return response.text.strip()


@functools.lru_cache(maxsize=100)
def get_explanation(topic: str) -> str:
    """Get plain-language conceptual explanation."""
    if not topic or not str(topic).strip():
        return "Please provide a topic to get an explanation."

    try:
        return _explain_with_gemini(topic)
    except Exception as e:
        return f"Error while generating the explanation:\n{str(e)}"
