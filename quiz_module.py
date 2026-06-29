import os
import google.generativeai as genai

# extracting the api key from the .env file
api_key = os.getenv("GOOGLE_API_KEY")

# configuring the genai
if api_key:
    genai.configure(api_key=api_key)
else:
    print("Gemini API not configured. GOOGLE_API_KEY environment variable not found.")

# main function
def generate_quiz(topic: str, num_questions: int = 5) -> str:

    # if no topic is provided - edge case
    if not topic.strip():
        return "Please provide a topic to generate a quiz."

    try:
        # initializing the model - used gemini 2.5 flash model
        model = genai.GenerativeModel("gemini-2.5-flash")

        # prompt for quiz generation
        prompt = f"""
            You are an expert educational quiz generator. Create a quiz with exactly {num_questions} multiple-choice questions on the topic: "{topic}".

            For each question:
            1. Write a clear question
            2. Provide 4 options (A, B, C, D)
            3. Indicate the correct answer
            4. Give a brief explanation of why that answer is correct

            Format the output clearly and make it easy to read for students.
        """

        # obtaining the response - temp = 0.7 for more creative questions
        response = model.generate_content(prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7
            )
        )

        # returning the generated quiz
        return response.text.strip()

    # error handling
    except Exception as e:
        return f"Error while generating the quiz:\n{str(e)}"
