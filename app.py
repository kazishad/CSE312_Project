import re
from tabnanny import check
from flask import Flask, render_template, request, redirect, url_for
import os


import db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

@app.route("/")
def root():
    return "root"
@app.route("/<name>")
def name(name):
    return f"hello {name}"


@app.route("/login")
def login():
    return "login"


@app.route("/register", methods=["POST", "GET"])
def register():

    # with open('static/Register.html', 'r') as f:
    #     html_string = f.read()
    if request.method == "POST":
        form = request.form 
        # auth here
        db.Insert(form)
        return redirect(url_for("name", name=form["usernameField"]))
    else:
        return render_template("Register.html")

def check_allowed(input: str) -> bool:

    extensions = {'jpg', 'png', 'jpeg'}
    file_type = input.split('.')[1].lower()

    if file_type in extensions:
        return True
    else:
        return False

@app.route("/upload", methods=["POST","GET"])
def upload():
    if (request.method == "GET"):
        return render_template("upload_image.html")
    elif (request.method == "POST"):

        file = request.files['file']
        filename = file.filename

        if check_allowed(filename):

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Your File Has Been Saved!"
        else:
            return "Unsupported File Extension"

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
