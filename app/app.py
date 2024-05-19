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
    'Sabadell Plaça Major': ['english.mp3', 'sabadell_placa_major.jpg'],
    'Sabadell Parc del Nord': ['english.mp3', 'sabadell_parc_del_nord.jpg'],
    'Les Planes': ['english.mp3', 'les_planes.jpg'],
    'La Creu Alta': ['english.mp3', 'la_creu_alta.jpg'],
}

follow = [{'lat': 41.38563194, 'long': 2.168720219, 'name': 'Plaça Catalunya'},
 {'lat': 41.39281434, 'long': 2.158030869, 'name': 'Provença'},
 {'lat': 41.39909823, 'long': 2.152662325, 'name': 'Gràcia'},
 {'lat': 41.40106608, 'long': 2.147133783, 'name': 'Sant Gervasi'},
 {'lat': 41.39852644, 'long': 2.142346041, 'name': 'Muntaner'},
 {'lat': 41.39781569, 'long': 2.136433966, 'name': 'La Bonanova'},
 {'lat': 41.39780042, 'long': 2.130811822, 'name': 'Les Tres Torres'},
 {'lat': 41.39849938, 'long': 2.125574875, 'name': 'Sarrià'},
 {'lat': 41.40921616, 'long': 2.111181541, 'name': 'Peu del Funicular'},
 {'lat': 41.42009441, 'long': 2.096936777, 'name': 'Baixador de Vallvidrera'},
 {'lat': 41.42740264, 'long': 2.0916176, 'name': 'Les Planes'},
 {'lat': 41.44487408, 'long': 2.073166144, 'name': 'La Floresta'},
 {'lat': 41.45784156, 'long': 2.06831203, 'name': 'Valldoreix'},
 {'lat': 41.46791038, 'long': 2.078203288, 'name': 'Sant Cugat Centre'},
 {'lat': 41.481248, 'long': 2.072928, 'name': 'Volpelleres'},
 {'lat': 41.49015388, 'long': 2.076498641, 'name': 'Sant Joan'},
 {'lat': 41.50085844, 'long': 2.090556583, 'name': 'Bellaterra'},
 {'lat': 41.50285282, 'long': 2.102510441, 'name': 'Universitat Autònoma'},
 {'lat': 41.52999155, 'long': 2.088722533, 'name': 'Sant Quirze'},
 {'lat': 41.542522966, 'long': 2.100463866, 'name': 'Can Feu | Gràcia'},
 {'lat': 41.547519, 'long': 2.103258, 'name': 'Sabadell Plaça Major'},
 {'lat': 41.554571, 'long': 2.102618, 'name': 'La Creu Alta'},
 {'lat': 41.561225, 'long': 2.096657, 'name': 'Sabadell Nord'},
 {'lat': 41.571291, 'long': 2.089499, 'name': 'Sabadell Parc del Nord'}]

index = 0

with open('static/stations_s2.json', 'r', encoding='utf-8') as file:
    lat_long_stations = json.load(file)

with open('static/station2idx.json', 'r', encoding='utf-8') as file:
    station2idx = json.load(file)
    
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
    #latitude = data.get('latitude')
    #longitude = data.get('longitude')
    global follow
    if len(follow) == 0:
        follow = [{'lat': 41.38563194, 'long': 2.168720219, 'name': 'Plaça Catalunya'}, {'lat': 41.39281434, 'long': 2.158030869, 'name': 'Provença'}, {'lat': 41.39909823, 'long': 2.152662325, 'name': 'Gràcia'}, {'lat': 41.40106608, 'long': 2.147133783, 'name': 'Sant Gervasi'}, {'lat': 41.39852644, 'long': 2.142346041, 'name': 'Muntaner'}, {'lat': 41.39781569, 'long': 2.136433966, 'name': 'La Bonanova'}, {'lat': 41.39780042, 'long': 2.130811822, 'name': 'Les Tres Torres'}, {'lat': 41.39849938, 'long': 2.125574875, 'name': 'Sarrià'}, {'lat': 41.40921616, 'long': 2.111181541, 'name': 'Peu del Funicular'}, {'lat': 41.42009441, 'long': 2.096936777, 'name': 'Baixador de Vallvidrera'}, {'lat': 41.42740264, 'long': 2.0916176, 'name': 'Les Planes'}, {'lat': 41.44487408, 'long': 2.073166144, 'name': 'La Floresta'}, {'lat': 41.45784156, 'long': 2.06831203, 'name': 'Valldoreix'}, {'lat': 41.46791038, 'long': 2.078203288, 'name': 'Sant Cugat Centre'}, {'lat': 41.481248, 'long': 2.072928, 'name': 'Volpelleres'}, {'lat': 41.49015388, 'long': 2.076498641, 'name': 'Sant Joan'}, {'lat': 41.50085844, 'long': 2.090556583, 'name': 'Bellaterra'}, {'lat': 41.50285282, 'long': 2.102510441, 'name': 'Universitat Autònoma'}, {'lat': 41.52999155, 'long': 2.088722533, 'name': 'Sant Quirze'}, {'lat': 41.542522966, 'long': 2.100463866, 'name': 'Can Feu | Gràcia'}, {'lat': 41.547519, 'long': 2.103258, 'name': 'Sabadell Plaça Major'}, {'lat': 41.554571, 'long': 2.102618, 'name': 'La Creu Alta'}, {'lat': 41.561225, 'long': 2.096657, 'name': 'Sabadell Nord'}, {'lat': 41.571291, 'long': 2.089499, 'name': 'Sabadell Parc del Nord'}]
    next = follow.pop(0)
    latitude, longitude, name = next['lat'], next['long'], next['name']
    next_station_index = station2idx[name]
    direction = 1
    
    #next_station_index = session.get('next_station_index')
    #direction = session.get('direction')
    
    #if next_station_index is None or direction is None:
    #    next_station_index, direction = logic_app(latitude, longitude)
    #    session['next_station_index'] = next_station_index
    #    session['direction'] = direction
    
    next_station_index = update_next_station_index(next_station_index, direction, latitude, longitude)

    session['next_station_index'] = next_station_index

    station_name = lat_long_stations['stations'][next_station_index]['name']
    audio_file, image_file = stations[station_name]
    print(next_station_index)
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
