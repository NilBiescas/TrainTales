import os
import torch
from openvoice import se_extractor
from melo.api import TTS

# Paths and device setup
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Function to create the necessary directories
def create_output_directory(station_name):
    output_dir = os.path.join('train_stories', station_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Function to convert text to speech and save the files
def generate_story_for_station(station_name, texts, speed=1.0):
    output_dir = create_output_directory(station_name)
    
    # Mapping for filenames
    filenames = {
        'EN_NEWEST': 'english.mp3',
        'ES': 'spanish.mp3'
    }

    # Process each language
    for language, text in texts.items():
        model = TTS(language=language, device=device)
        speaker_ids = model.hps.data.spk2id
        
        for speaker_key in speaker_ids.keys():
            speaker_id = speaker_ids[speaker_key]
            speaker_key = speaker_key.lower().replace('_', '-')
            
            model.tts_to_file(text, speaker_id, filenames[language], speed=speed)
            
            # Save the output file in the specified directory
            save_path = os.path.join(output_dir, filenames[language])
            os.rename(filenames[language], save_path)
            
            # Only need one speaker per language, break after first
            break

# Texts to be converted to speech
texts = {
    'EN_NEWEST': '''What an adventure you're on! You're in Vallbona, a special neighborhood in Barcelona! Did you know that Vallbona is like a treasure chest filled with history and secrets? Let me tell you a fun fact: Vallbona has been around for over 1,000 years! That's even older than some of the buildings you might see in Barcelona! The name "Vallbona" comes from the Latin words "vallis" meaning "valley" and "bona" meaning "good". So, Vallbona means "good valley"! Can you imagine what it was like to live here centuries ago? This area was once home to ancient Romans, and later on, it was a place where farmers grew grapes, olives, and other yummy food. The valley was also an important spot for merchants who came to trade goods. Today, Vallbona is a thriving neighborhood with parks, schools, and even a really cool old church called Sant Pere de Vallbona! You might want to ask your parents to take you to see it when you get off the train. As we ride the train, look out the window and see if you can spot the hills and valleys that give Vallbona its unique landscape. It's like a big puzzle, and you're a part of it! What do you think, are you excited to explore more of Vallbona and Barcelona?''',
    'ES': '''Hola buenos días, ¿cómo estás? Espero que estés bien. Hoy vamos a hablar sobre la importancia de la educación en la vida de las personas. La educación es un pilar fundamental en el desarrollo de las personas, ya que nos permite adquirir conocimientos, habilidades y valores que nos ayudan a crecer y a ser mejores seres humanos.'''
}

# Example usage
station_name = 'plaça catalunya'
generate_story_for_station(station_name, texts)
