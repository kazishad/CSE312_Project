from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from custom_websockets import *
from flask_socketio import SocketIO, emit

import db

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def root():
    return "root"
@app.route("/<name>")
def name(name):
    return f"hello {name}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        form = request.form 
        print(form)
    else:
        return render_template("Login.html")

    return redirect(url_for("root"))


@app.route("/register", methods=["POST", "GET"])
def register():

    # with open('static/Register.html', 'r') as f:
    #     html_string = f.read()
    if request.method == "POST":
        form = request.form 
        print(form)
        # auth here
        # db.Insert(form)
        return redirect(url_for("name", name=form["usernameField"]))
    else:
        return render_template("Register.html")

# ---------------------------------------------------------------------------------
@socketio.on('connect')
def chat_connect():
    print ('connected')


@socketio.on('disconnect')
def chat_disconnect():
    print ("Client disconnected")


@socketio.on('broadcast')
def chat_broadcast(message):
    print ("test")
    emit("chat", {'data': message['data']})


@socketio.on('message')
def handle_message(data):
    handle_websockets(data)


if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    socketio.run(app)