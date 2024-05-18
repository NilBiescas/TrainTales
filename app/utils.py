import requests
import math
import json

stations_index = ['PC', 'PR', 'GR', 'SG', 'MN', 'BN', 'TT', 'SR', 'PF', 'VL', 'LP', 'LF', 'VD', 'SC', 'VO', 'SJ', 'BT', 'UN', 'SQ', 'CF', 'PJ', 'CT', 'NO', 'PN']

# Define the endpoint URL for the FGC stations dataset
endpoint_url = 'https://dadesobertes.fgc.cat/api/records/1.0/search/'


with open('static\idx2station.json', 'r', encoding='utf-8') as file:
    idx2station = json.load(file)
    
with open('static\stations_s2.json', 'r', encoding='utf-8') as file:
    lat_long_stations = json.load(file)

path_json = 'static\codis_info_lineas.json'
with open(path_json, 'r', encoding='utf-8') as file:
    codes2info_lines = json.load(file)

def get_station_name_by_code(station_code):
    # Set up the parameters
    params = {
        'dataset': 'codigo-estaciones',
        'q': station_code,
        'rows': 1  # Assuming station codes are unique, fetch one record
    }

    # Make the request
    response = requests.get(endpoint_url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data['records']:
            fields = data['records'][0]['fields']
            return fields['nom_estacio']
        else:
            return "Station not found"
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_next_stations(my_train):
    stations = my_train['fields']['properes_parades']
    stations = stations.split(';')
    nex_stations = eval(stations[0])['parada']
    return nex_stations

def get_trains(rows = 100, line = 'S2'):
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
    else:
        print("Error:", response.status_code, response.text)
    return train_data

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon1 - lon2)
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
    """Get the train closest to the user's location
    The output is a dict with the following keys:
    dict_keys(['datasetid', 'recordid', 'fields', 'geometry', 'record_timestamp'])
    """
    trains_information = get_trains()
    nearest_train = get_my_train(user_lat = user_lat, 
                            user_lon = user_lon, 
                            trains_information = trains_information)
    # Get my train
    for train in trains_information['records']:
        if train['fields']['id'] == nearest_train['id']:
            my_train = train
            break
    return my_train

def in_station(index_station, our_lat, our_lon):
    abrebiation_station = index_station
    result = lat_long_stations['stations'][abrebiation_station]
    lat, long = result['lat'], result['long']
    distance = haversine(our_lat, our_lon, lat, long)
    if distance < 0.1: # Comprobar distancia
        return True
    return False

def update_next_station_index(next_station_index, direction, latitude, longitude):
    if in_station(next_station_index, latitude, longitude):
        next_station_index += direction
    return next_station_index
    
def init_station(init_lat, init_lon):
    my_train = get_train(user_lat = init_lat, user_lon = init_lon)
    next_stations = get_next_stations(my_train)
    desti = my_train['fields']['desti']
    direction = 1 if desti == stations_index[-1] else -1
    next_station_index = stations_index.index(next_stations)
    return next_station_index, direction

def logic_app(latitude, longitude):
    next_station_index, desti = init_station(latitude, longitude)

    direction = 1 if desti == stations_index[-1] else -1
    next_station_index = stations_index[next_station_index]
    # next_station_index = stations_index.index(next_stations)
    return next_station_index, direction
