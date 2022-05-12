from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



@socketio.on('my event')
def handle_message(data):
    print('received message: ' + str(data), flush=True)
    dataaa= "this is kevin"
    socketio.emit('chat',{'data':dataaa});
    # send(dataaa, namespace='/chat')

@app.route('/')
def hello():
    return render_template('ss.html')

@socketio.on('connect')
def test_connect(auth):
    print("hihi--" , flush=True)
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # app.run(debug=True, host='0.0.0.0', port=port)