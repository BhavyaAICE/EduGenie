import os
from google import genai

# extracting the api key from the .env file
api_key = os.getenv("GOOGLE_API_KEY")

# configuring the genai client
if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None
    print("Gemini Api not configured. Environment Variable not found")

import functools

# main function
@functools.lru_cache(maxsize=100)
def get_summary(text: str, length: str = "medium") -> str:

    # if no text is provided - edge case
    if not text.strip():
        return "You need to provide a string to get the summary"


    try:    
        if not client:
            return "Gemini API key is missing."

        length_guides = {
            "short": "Provide a very concise summary (around 3-5 punchy bullet points) capturing only the core takeaways for fast revision.",
            "medium": "Provide a balanced, structured summary with key concepts, bullet points, and brief explanations.",
            "detailed": "Provide an in-depth, thorough summary covering all nuances, mechanisms, terminology, and key takeaways with clean section headers and bullet points."
        }
        guide = length_guides.get(str(length).lower(), length_guides["medium"])

        # prompt for summary generation
        prompt = f"""
            You are an expert educational assistant. Summarize the following educational text according to this guideline:
            {guide}

            Format your response cleanly using markdown (bold key terms, clean bullet points, clear headings where appropriate).
            Avoid unnecessary intro/outro filler.

            Text to summarize:
            {text}
        """

        # obtaining the response - temp = 0.5
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.5
            )
        )

        # returning the generated summary
        return response.text.strip()

    # error handling
    except Exception as e:
        return f"Error while generating the summary:\n{str(e)}"
