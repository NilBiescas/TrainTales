import os
import torch
from melo.api import TTS
from groq_api import get_model_response

# Paths and device setup
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Function to create the necessary directories
def create_output_directory(station_name):
    output_dir = os.path.join('train_stories', station_name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

# Function to convert text to speech and save the files
def generate_story_for_station(station_name, speed=1.0):
    output_dir = create_output_directory(station_name)
    
    # Languages and their corresponding filenames
    languages = {
        'EN': 'english.mp3',
        'ES': 'spanish.mp3'
    }

    # Process each language
    for lang_code, filename in languages.items():
        language = "English" if lang_code == 'EN' else "Spanish"
        text = get_model_response(station_name, language=language)
        
        model = TTS(language=lang_code, device=device)
        speaker_ids = model.hps.data.spk2id
        
        for speaker_key in speaker_ids.keys():
            speaker_id = speaker_ids[speaker_key]
            speaker_key = speaker_key.lower().replace('_', '-')
            
            model.tts_to_file(text, speaker_id, filename, speed=speed)
            
            # Save the output file in the specified directory
            save_path = os.path.join(output_dir, filename)
            os.rename(filename, save_path)
            
            # Only need one speaker per language, break after first
            break

# Example usage
station_names = ["Vallbona", "Universitat Autónoma", "Sant Cugat"]

s2_stations = [
    "Barcelona Plaça Catalunya",
    "Provença",
    "Gràcia",
    "Sant Gervasi",
    "Muntaner",
    "La Bonanova",
    "Les Tres Torres",
    "Sarrià",
    "Peu del Funicular",
    "Baixador de Vallvidrera",
    "Les Planes",
    "La Floresta",
    "Valldoreix",
    "Sant Cugat",
    "Volpelleres",
    "Sant Joan",
    "Bellaterra",
    "Universitat Autònoma",
    "Sant Quirze",
    "Can Feu | Gràcia",
    "Sabadell Plaça Major",
    "La Creu Alta",
    "Sabadell Nord",
    "Sabadell Parc del Nord"
]
for station_name in s2_stations:
    generate_story_for_station(station_name, speed=1.1)