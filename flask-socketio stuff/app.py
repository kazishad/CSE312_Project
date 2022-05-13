from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

localStorage= []

@app.route('/', methods=[ "GET"])
def root():
    return render_template('ss.html')

#This is used to obatin the message from js and obatin connection data
@socketio.on('connected-event')
def handle_message(data):
    print('received message: ' + str(data), flush=True)
    # socketio.emit('chat',{'data':dataaa})
    # send(dataaa, namespace='/chat')

@socketio.on('connect')
def test_connect(auth):
    print("hihi--" , flush=True)
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(data, flush=True)
    localStorage.append(data)
    print(localStorage, flush=True)
    emit('enterRoom',username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit(username + ' has left the room.', to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
