from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

stations = {'Barcelona Plaça Catalunya': ['english.mp3', 'pl_cat.jpg'],
            'Provença': ['english.mp3', 'provença.png'],}

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
    return "Provença"

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
    print(station_name, audio_file, image_file)
    return render_template('playing.html', station_name=station_name, audio_file=audio_file, image_file=image_file)


if __name__ == '__main__':
    app.run(debug=True)
