import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Function to make an API call and get the response from the model
def get_model_response(station_name, language="EN", previous_description="", underground=False):
    # Create the base system message
    base_message = f"You are a touristic guide talking to a kid of 8 years old who is using the train to travel with his family. Your objective is to tell the kid relevant information about the place he is visiting in such a way that he can understand it and be engaged with the story. The kid is arriving at the station {station_name} in Barcelona. "
    
    # Modify the message based on the underground flag
    if underground:
        base_message += "The station is underground, so describe interesting facts about the area above and any relevant historical or fun stories, but obviously don't tell him/her to look around because nothing can be seen. Please do it entirely in {language}. Ensure the story feels like a continuation if there was a previous description, don't welcome the kid again if it's not the first station."
    else:
        base_message += "Describe what the kid can see through the window, include interesting landmarks, historical facts, and any fun stories about the surroundings. Please do it entirely in {language}. Ensure the story feels like a continuation if there was a previous description, don't welcome the kid again if it's not the first station."

    # Make an API call to the chat endpoint
    messages = [{
        "role": "system",
        "content": base_message
    }]

    if previous_description:
        messages.append({
            "role": "assistant",
            "content": f"Previously, we already visited and talked about other station: {previous_description}"
        })

    messages.append({
        "role": "user",
        "content": f"Hi, I'm an 8-year-old kid and I’m on a train with my family. We’re just arriving at {station_name} station in Barcelona. I'm looking through the window. Can you tell me something interesting about what I can see and the history of this place?"
    })
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    # Return the response from the model
    return chat_completion.choices[0].message.content

if __name__ == "__main__":
    station_name = "Vallbona"
    previous_description = ""
    print(get_model_response(station_name, language="EN", previous_description=previous_description, underground=False))
