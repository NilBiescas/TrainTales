import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

def generate_quiz_prompt(station_name, language="EN"):
    """
    Generates a prompt for the Groq API to create 5 multiple choice questions.
    """
    return [
        f"""You are a helpful AI assistant tasked with designing a fun quiz for kids about train travel. 
        Create 5 multiple choice questions related to the {station_name} station in Barcelona. 
        Each question should have 4 answer choices (A, B, C, D) with only one correct answer. 
        Focus on interesting landmarks, historical facts, or fun stories about the surroundings. 
        Format the output as a JSON object with the following structure:

        ```json
        {{
            "questions": [
                {{
                    "question": "Question text",
                    "choices": {{
                        "A": "Choice A",
                        "B": "Choice B",
                        "C": "Choice C",
                        "D": "Choice D"
                    }},
                    "correct": "Correct answer letter" 
                }},
                // ... more questions
            ]
        }}
        ``` 

        Ensure the questions are engaging and appropriate for an 8-year-old child.
        Use {language} for the questions and answers. THE ONLY THING YOU SHOULD OUTPUT is the JSON object with the questions.
        """
    ]

def get_quiz_questions(station_name, language="EN"):
    """
    Calls the Groq API to generate the multiple choice questions.
    """
    prompt = generate_quiz_prompt(station_name, language)
    response = model.generate_content(prompt)
    return response.text
