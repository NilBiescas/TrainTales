from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import random
import os
app = Flask(__name__)

stations = {'Barcelona Plaça Catalunya': ['english.mp3', 'pl_cat.jpg'],
            'Provença': ['english.mp3', 'provença.png'],
            'Gràcia': ['english.mp3', 'gracia.jpg'],
            'Sant Gervasi': ['english.mp3', 'sant_gervasi.jpg'],
            'Muntaner': ['english.mp3', 'muntaner.jpg'],
            'La Bonanova': ['english.mp3', 'la_bonanova.jpeg'],
            'Les Tres Torres': ['english.mp3', 'les_tres_torres.jpg'],
            'Sarrià': ['english.mp3', 'sarria.jpg'],
            'Peu del Funicular': ['english.mp3', 'peu_de_funicular.jpg'],
            'Baixador de Vallvidrera': ['english.mp3', 'vallvidrera.jpg'],
            'Les Planes': ['english.mp3', 'les_planes.jpg'],
            'La Floresta': ['english.mp3', 'la_floresta.jpg'],
            'Valldoreix': ['english.mp3', 'valldoreix.jpg'],
            'Sant Cugat': ['english.mp3', 'sant_cugat.jpg'],
            'Volpelleres': ['english.mp3', 'volpelleres.jpg'],
            'Sant Joan': ['english.mp3', 'sant_joan.jpeg'],
            'Bellaterra': ['english.mp3', 'bellaterra.jpg'],
            'Universitat Autònoma': ['english.mp3', 'uab.jpg'],
            'Sant Quirze': ['english.mp3', 'sant_quirze.jpg'],
            }

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

def get_station():
    # Random station
    return random.choice(list(stations.keys()))
    #return "Provença"

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude, 'station_name': 'Barcelona Plaça Catalunya'})

@app.route('/playing')
def playing():
    station_name = get_station()
    audio_file, image_file = stations[station_name]
    return render_template('playing.html', station_name=station_name, audio_file=audio_file, image_file=image_file)


@app.route('/quiz/<station_name>')
def quiz(station_name):
    quiz_file_path = f'app/quizzes/{station_name}/en_quiz.json'
    with open(quiz_file_path, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    return render_template('quiz.html', station_name=station_name, quiz_data=quiz_data)


if __name__ == '__main__':
    app.run(debug=True)

