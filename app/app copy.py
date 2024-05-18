from flask import Flask, render_template, request, jsonify, session
import random
import os
import json
from app.utils import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for using sessions

stations = {
    'Barcelona Plaça Catalunya': ['english.mp3', 'pl_cat.jpg'],
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

@app.route('/')
def index():
    # Initialize session variables to None if they are not already set
    session['next_station_index'] = None
    session['direction'] = None
    print("Sessions values:", session.get('next_station_index'), session.get('direction'))
    return render_template('home.html')



@app.route('/location', methods=['POST'])
def location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    next_station_index = session.get('next_station_index')
    direction = session.get('direction')
    print("Sessions values 2:", next_station_index, direction)
    
    if next_station_index is None or direction is None:
        next_station_index, direction = logic_app(latitude, longitude)
        session['next_station_index'] = next_station_index
        session['direction'] = direction
    
    latitude = 41.5474198
    longitude = 2.1088815
    
    next_station_index = update_next_station_index(next_station_index, direction, latitude, longitude)
    print(next_station_index, direction)

    session['next_station_index'] = next_station_index

    return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude})

@app.route('/playing')
def playing():
    station_name = ""#get_station()
    audio_file, image_file = stations[station_name]
    return render_template('playing.html', station_name=station_name, audio_file=audio_file, image_file=image_file)

@app.route('/quiz/<station_name>')
def quiz(station_name):
    quiz_file_path = os.path.join('quizzes', station_name, 'english_gemini_quiz.json')
    if not os.path.exists(quiz_file_path):
        return jsonify({'error': 'Quiz not found'}), 404

    with open(quiz_file_path, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)

    return render_template('quiz.html', station_name=station_name, quiz_data=quiz_data)

if __name__ == '__main__':
    app.run(debug=True)
