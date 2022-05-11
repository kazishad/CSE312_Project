import re
from tabnanny import check
from flask import Flask, request, redirect, url_for
import os
from authentication import auth_token
import save_picture

from logout import *
from authentication import *

import db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

@app.route("/")
def root():
    return "<h1>root</h1>"
@app.route("/<name>")
def name(name):
    # check 
    return f"hello {name}"


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        form = request.form 
        print(form)
    else:
        with open("templates/Login.html") as f:
            return f.read()
    return redirect(url_for("root"))

@app.route("/logout", methods=["POST"])
def logout():
    auth_token = request.headers.get("auth_token") # Obtain auth token
    success, username = username_from_auth_token(auth_token) # Obtain username by auth token
    if success:
        logout_user(username)
        return "You are now logged out. Hope to see you again soon!"
    else:
        return "Unable to Logout: invalid auth_token"

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
        with open("templates/Register.html") as f:
            return f.read()

def check_allowed(input: str) -> bool:
    extensions = {'jpg', 'png', 'jpeg'}
    print(f"check_allowed input {input}", flush=True)
    file_type = input.split('.')[1].lower()
    return file_type in extensions

@app.route("/upload", methods=["POST","GET"])
def upload():
    if (request.method == "GET"):
        with open("templates/upload_image.html") as f:
            return f.read()
    elif (request.method == "POST"):
        file = request.files['file']
        input_name = file.filename
        print(f"input_name:{input_name}",flush=True)
        extension_type = input_name.split(".")[1]
        if not check_allowed(input_name):
            return f"Wrong file type uploaded, <br/>Allowed file type are: jpg, png, and jpeg <br/>The uploaded file type is: {extension_type}"
        filename = "picture" + save_picture.get_id() + "." + str(extension_type)
        save_picture.picture_location(filename)
        print("this is the filename", filename,flush=True)
        s = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(s)
        return "Your File Has Been Saved!"

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
