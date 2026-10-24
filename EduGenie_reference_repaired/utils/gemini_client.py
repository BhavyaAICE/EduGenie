"""
EduGenie Shared Gemini Client Initializer
"""

import os
from google import genai
from dotenv import load_dotenv

load_dotenv()


def get_gemini_client():
    """Retrieve an initialized Google GenAI client instance."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Warning: GOOGLE_API_KEY environment variable not set.")
        return None
    return genai.Client(api_key=api_key)
