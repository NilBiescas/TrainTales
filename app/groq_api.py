import os
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Function to make an api call and get the response from the model
def get_model_response(user_input=None, user_data=None):
    
    # Make an API call to the chat endpoint
    messages = []
    
    '''if user_data:
        messages.append({
            "role": "system",
            "content": f"You are talking to a person of {user_data['age']} years old, is a person who likes the following topics: {user_data['likes']} and\
                        prefers {user_data['learning_preference']}% of theory and {100 - user_data['learning_preference']}% of examples and practice in the explanations,\
                        so respond accordingly. Take into account this information to provide better personalized explanations."
        })'''
    
    messages.append({
            "role": "system",
            "content": "You are a touristic guide talking to a kid of 8 years old who is using the train to travell with his family. Your objective is to tell the kid relevant information about the place he is visiting in such a way that he can understand it and be engaged with the story. Take into account that the station where this kid is is Vallbona, from Barcelona."}),

    # Append the current user input to the message history
    messages.append({
        "role": "user",
        "content": "I am a kid of 8 years old traveling around Vallbona, Barcelona. Can you tell me something interesting about this place?",
    })
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-70b-8192",
    )

    # Return the response from the model
    return chat_completion.choices[0].message.content

if __name__ == "__main__":

    # Print the response from the model

    print(get_model_response())
