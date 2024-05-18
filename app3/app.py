from flask import Flask, render_template, request, jsonify
import requests
import json
import math

app = Flask(__name__)

endpoint_url = 'https://dadesobertes.fgc.cat/api/records/1.0/search/'

path_json = r'C:\Users\Maria\Desktop\HackathonUAB\UABHACK\train_infor\codis_info_lineas.json'
with open(path_json, 'r') as file:
    codes2info_lines = json.load(file)


def get_trains(rows = 100, line = 'S2'):
    # Define the endpoint URL for train localization

    # Set up the parameters
    params = {
        'dataset': 'posicionament-dels-trens',
        'rows': rows,  # Number of records to fetch
        'q': f'lin:{line}'  # Replace LINE_ID with the specific line you want to filter by
    }

    # Make the request
    response = requests.get(endpoint_url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        train_data = response.json()       
        return train_data
    else:
        # print("Error:", response)
        raise Exception(f"Error: {response.status_code}, {response.text}")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_my_train(user_lat, user_lon, trains_information):
    trains_info = []
    for data in trains_information['records']:   
        geo = data['fields']['geo_point_2d']
        trains_info.append({'id': data['fields']['id'], 'lat': geo[0], 'lon': geo[1]})
    
    nearest_train = None
    min_distance = float('inf')

    for train in trains_info:
        distance = haversine(user_lat, user_lon, train['lat'], train['lon'])
        if distance < min_distance:
            min_distance = distance
            nearest_train = train
    return nearest_train

def get_train(user_lat, user_lon):
    trains_information = get_trains()
    nearest_train = get_my_train(user_lat=user_lat, user_lon=user_lon, trains_information=trains_information)
    for train in trains_information['records']:
        if train['fields']['id'] == nearest_train['id']:
            my_train = train
            break
    return my_train

def get_next_stations(my_train):
    stations = my_train['fields']['properes_parades']
    print(stations)
    stations = stations.split(';')
    nex_stations = eval(stations[0])['parada']
    return get_station_name_by_code(nex_stations)

def get_station_name_by_code(station_code):
    # Set up the parameters
    params = {
        'dataset': 'codigo-estaciones',
        'q': station_code,
        'rows': 1
    }

    endpoint_url = 'https://example.com/api'  # Replace with actual endpoint URL
    response = requests.get(endpoint_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['records']:
            fields = data['records'][0]['fields']
            return fields['nom_estacio']
        else:
            return "Station not found"
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    # my_train = get_train(latitude, longitude)
    # print(my_train)
    # station_name = get_next_stations(my_train)
    station_name = "Bonanova"
    latitude = 41.394768
    longitude = 2.134088
    print(station_name)
    return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude, 'station_name': station_name})

if __name__ == '__main__':
    app.run(debug=True)
