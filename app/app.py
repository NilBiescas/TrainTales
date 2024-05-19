from flask import Flask, render_template, request, jsonify, session
import json
import random
import os
from utils import *

app = Flask(__name__)
app.secret_key = 'supersecretkey'

stations = {
    'Plaça Catalunya': ['english.mp3', 'pl_cat.jpg'],
    'Provença': ['english.mp3', 'provença.png'],
    'Gràcia': ['english.mp3', 'gracia.jpg'],
    'Sant Gervasi': ['english.mp3', 'sant_gervasi.jpg'],
    'Muntaner': ['english.mp3', 'muntaner.jpg'],
    'La Bonanova': ['english.mp3', 'la_bonanova.jpeg'],
    'Les Tres Torres': ['english.mp3', 'les_tres_torres.jpg'],
    'Sarrià': ['english.mp3', 'sarria.jpg'],
    'Peu del Funicular': ['english.mp3', 'peu_de_funicular.jpg'],
    'Baixador de Vallvidrera': ['english.mp3', 'vallvidrera.jpg'],
    'Valldoreix': ['english.mp3', 'valldoreix.jpg'],
    'La Floresta': ['english.mp3', 'la_floresta.jpg'],
    'Sant Cugat Centre': ['english.mp3', 'sant_cugat.jpg'],
    'Volpelleres': ['english.mp3', 'volpelleres.jpg'],
    'Sant Joan': ['english.mp3', 'sant_joan.jpeg'],
    'Bellaterra': ['english.mp3', 'bellaterra.jpg'],
    'Universitat Autònoma': ['english.mp3', 'uab.jpg'],
    'Sant Quirze': ['english.mp3', 'sant_quirze.jpg'],
    'Can Feu | Gràcia': ['english.mp3', 'can_feu.jpg'],
    'Sabadell Nord': ['english.mp3', 'sabadell_nord.jpg'],
    'Sabadell Parc del Nord': ['english.mp3', 'sabadell_parc_del_nord.jpg']
}

with open('static/stations_s2.json', 'r', encoding='utf-8') as file:
    lat_long_stations = json.load(file)

@app.route('/')
def index():
    
    session['next_station_index'] = None
    session['direction'] = None
    audio_file, image_file = '', ''
    station_name = ''
    return render_template('home.html', station_name=station_name, audio_file=audio_file, image_file=image_file)

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    next_station_index = session.get('next_station_index')
    direction = session.get('direction')
    
    if next_station_index is None or direction is None:
        next_station_index, direction = logic_app(latitude, longitude)
        session['next_station_index'] = next_station_index
        session['direction'] = direction
    
    next_station_index = update_next_station_index(next_station_index, direction, latitude, longitude)

    session['next_station_index'] = next_station_index

    station_name = lat_long_stations['stations'][next_station_index]['name']
    audio_file, image_file = stations[station_name]
    print('image_file:', image_file)
    return jsonify({'status': 'success', 'latitude': latitude, 
                    'longitude': longitude, 'audio_file': audio_file, 'image_file': image_file,
                    'next_station_name': station_name})

@app.route('/quiz/<station_name>')
def quiz(station_name):
    quiz_file_path = f'app/quizzes/{station_name}/en_quiz.json'
    with open(quiz_file_path, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    return render_template('quiz.html', station_name=station_name, quiz_data=quiz_data)

if __name__ == '__main__':
    app.run(debug=True)
