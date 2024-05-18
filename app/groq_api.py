import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Function to make an API call and get the response from the model
def get_model_response(station_name, language="EN"):
    # Make an API call to the chat endpoint
    messages = [{
        "role": "system",
        "content": f"You are a touristic guide talking to a kid of 8 years old who is using the train to travel with his family. Your objective is to tell the kid relevant information about the place he is visiting in such a way that he can understand it and be engaged with the story. The kid is arriving at the station {station_name} in Barcelona. Describe what the kid can see through the window, include interesting landmarks, historical facts, and any fun stories about the surroundings. You should answer entirely in {language}"
    }, {
        "role": "user",
        "content": f"Hi, I'm an 8-year-old kid and I’m on a train with my family. We’re just arriving at {station_name} station in Barcelona. I'm looking through the window. Can you tell me something interesting about what I can see and the history of this place? Do it in {language}"
    }]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    # Return the response from the model
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    station_name = "Vallbona"
    print(get_model_response(station_name, language="EN"))

