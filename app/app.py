from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

status = "Stopped"

@app.route('/')
def index():
    return render_template('index.html', status=status)

@app.route('/play', methods=['POST'])
def play():
    global status
    status = "Playing..."
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    global status
    status = "Stopped"
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
