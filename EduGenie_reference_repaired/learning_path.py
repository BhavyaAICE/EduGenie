"""
EduGenie Learning Path & Curriculum Roadmap Module (Repaired)
"""

import os
import json
import functools
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


# Repaired Signature: topic is parameter 1, level is parameter 2 with default "beginner"
@functools.lru_cache(maxsize=100)
def get_learning_path(topic: str, level: str = "beginner") -> dict:
    """Generate structured educational curriculum roadmap."""
    if not topic or not str(topic).strip():
        return {"error": "Please provide a topic to generate a learning path."}

    if not client:
        return {"error": "Gemini API key is missing. Please set GOOGLE_API_KEY in your environment."}

    try:
        prompt = f"""
            You are an expert educational advisor. Create a personalized and structured learning roadmap for the topic: "{topic}".
            The student's current level is: {level}.

            IMPORTANT: Return ONLY valid JSON in this exact format, no other text:
            {{
                "topic": "{topic}",
                "level": "{level}",
                "roadmap": [
                    {{
                        "phase": "Phase 1: Foundations",
                        "description": "Brief description of this phase.",
                        "topics": ["Topic 1", "Topic 2", "Topic 3"],
                        "estimated_time": "e.g., 2 weeks",
                        "resources": ["Resource 1", "Resource 2"]
                    }},
                    {{
                        "phase": "Phase 2: Intermediate Concepts",
                        "description": "Brief description...",
                        "topics": ["Topic A", "Topic B"],
                        "estimated_time": "e.g., 4 weeks",
                        "resources": ["Resource 3", "Resource 4"]
                    }}
                ]
            }}

            Rules:
            - Create 4 to 6 logical sequential phases from start to finish
            - Keep the descriptions concise and motivating
            - List 2 to 4 key topics per phase
            - Provide 1 to 2 realistic resources per phase
            - Return ONLY the JSON, no markdown, no code blocks
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.6
            )
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.split("\n", 1)[1]
            raw_text = raw_text.rsplit("```", 1)[0]
            raw_text = raw_text.strip()

        return json.loads(raw_text)

    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse roadmap data. Please try again.\n{str(e)}"}
    except Exception as e:
        return {"error": f"Error while generating the learning path:\n{str(e)}"}
