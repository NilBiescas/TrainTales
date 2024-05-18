from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('submit_answer')
def handle_answer(answer):
    correct_answer = 'A'
    if answer == correct_answer:
        response = {'answer': answer, 'correct': True}
    else:
        response = {'answer': answer, 'correct': False}
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app)
