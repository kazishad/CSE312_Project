import re
import sys
from tabnanny import check
import pymongo
from flask import Flask, render_template, request, redirect, url_for
import os
from save_picture import get_id, save_location
import db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'
myclient = pymongo.MongoClient("mongo")

@app.route("/", methods=["POST", "GET"])
def root():
    sys.stdout.flush()
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        form = request.form
        db.login_check(username= form["usernameField"], password= form["passwordField"])
        sys.stdout.flush()
        return redirect(url_for(".name", name=form["usernameField"]))

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        form = request.form
        db.create_new_user(username= form["usernameField"], password= form["passwordField"])
        sys.stdout.flush()
        return redirect(url_for(".name", name=form["usernameField"]))

@app.route("/onlineOffline", methods=['POST'])
def onlineOffline():
    form2 = request.json
    print(form2)
    sys.stdout.flush()
    return f"hi"

@app.route("/userHomPage/<name>")
def name(name):
    print(name)
    sys.stdout.flush()
    return render_template("userHomePage.html", userdata = name)

def check_allowed(input: str) -> bool:
    extensions = {'jpg', 'png', 'jpeg'}
    print(f"check_allowed input {input}", flush=True)
    file_type = input.split('.')[1].lower()
    return file_type in extensions

@app.route("/upload", methods=["POST","GET"])
def upload():
    if (request.method == "GET"):
        return render_template("upload_image.html")
    elif (request.method == "POST"):
        file = request.files['file']
        input_name = file.filename
        print(f"input_name:{input_name}",flush=True)
        extension_type = input_name.split(".")[1]
        if not check_allowed(input_name):
            return f"Wrong file type uploaded, <br/>Allowed file type are: jpg, png, and jpeg <br/>The uploaded file type is: {extension_type}"
        filename = "picture" + get_id() + "." + str(extension_type)
        save_location(filename)
        print("this is the filename", filename,flush=True)
        s = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(s)
        return "Your File Has Been Saved!"

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
