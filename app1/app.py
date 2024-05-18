from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    return jsonify({'status': 'success', 'latitude': latitude, 'longitude': longitude})

if __name__ == '__main__':
    app.run(debug=True)
