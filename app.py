import re
from tabnanny import check
from flask import Flask, make_response, render_template, request, redirect, url_for
import os
from save_picture import get_id, save_location




import db
from xsrf_tokens import generate_xsrf_token

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

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

def check_allowed(input: str) -> bool:
    extensions = {'jpg', 'png', 'jpeg'}
    print(f"check_allowed input {input}", flush=True)
    file_type = input.split('.')[1].lower()
    return file_type in extensions

@app.route("/upload", methods=["POST","GET"])
def upload():
    if (request.method == "GET"):
        xsrf_token = generate_xsrf_token()
        return render_template("upload_image.html", xsrf_token=xsrf_token)
    elif (request.method == "POST"):
        # TODO: Obtain the token from the request data
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
