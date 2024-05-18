import os
import json
from groq_quiz import get_quiz_questions
#from gemini_quiz import get_quiz_questions
# Stations for which to generate quizzes
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
    "Can Feu Gràcia Sabadell",
    "Sabadell Plaça Major",
    "La Creu Alta",
    "Sabadell Nord",
    "Sabadell Parc del Nord"
]

def generate_quiz_for_station(station_name, language="EN"):
    """
    Generates a quiz for a station and saves it to a file.
    """
    try:
        questions = get_quiz_questions(station_name, language)

        # Create output directory
        output_dir = os.path.join('quizzes', station_name)
        os.makedirs(output_dir, exist_ok=True)

        # Define filename based on language
        filename = f"{language.lower()}_quiz.json"

        # Save the quiz data to a JSON file
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(json.loads(questions), f, indent=4)

    except json.JSONDecodeError as e:
      print(f"Error decoding JSON for {station_name}: {e}")
      print(f"Raw API response: {questions}")

if __name__ == "__main__":
  for station in s2_stations:
    generate_quiz_for_station(station, "EN")
    #generate_quiz_for_station(station, "ES") # Uncomment to generate quizzes in Spanish as well