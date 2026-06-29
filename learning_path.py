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
def get_learning_path(topic: str, level: str = "beginner") -> str:

    # if no topic is provided - edge case
    if not topic.strip():
        return "Please provide a topic to generate a learning path."

    try:
        # initializing the model - used gemini 2.5 flash model
        model = genai.GenerativeModel("gemini-2.5-flash")

        # prompt for learning path generation
        prompt = f"""
            You are an expert educational advisor. Create a personalized and structured learning roadmap for the topic: "{topic}".
            The student's current level is: {level}.

            The learning path should include:
            1. Prerequisites (what the student should know before starting)
            2. Beginner topics and concepts to learn first
            3. Intermediate topics to progress to
            4. Advanced topics for mastery
            5. Recommended resources (books, websites, tools) for each stage
            6. Estimated time to complete each stage
            7. Practice projects or exercises for hands-on learning

            Format the output as a clear, structured roadmap that is easy to follow. Use bullet points and sections.
        """

        # obtaining the response - temp = 0.6
        response = model.generate_content(prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.6
            )
        )

        # returning the generated learning path
        return response.text.strip()

    # error handling
    except Exception as e:
        return f"Error while generating the learning path:\n{str(e)}"
