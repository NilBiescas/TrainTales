from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Replace with your actual coordinates
    markers = [
        {"lat": 41.40338, "lng": 2.17403},  # Example marker 1
        {"lat": 41.38506, "lng": 2.17340},  # Example marker 2
        # Add more markers here
    ]
    return render_template('index.html', markers=markers)

if __name__ == '__main__':
    app.run(debug=True)
