import re
from flask import Flask, request, redirect, url_for, make_response
import os
from save_picture import *
from authentication import *
from logout import *
from authentication import *

import db

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

@app.route("/", methods=["POST", "GET"])
def root():
    return "<h1>root</h1>"

    
@app.route("/<profile>")
def profile(profile):
    returnhtml = ""

    if check_user(profile):
        if "auth" in request.cookies:
            authToken = request.cookies.get('auth')
            user = username_from_auth_token(authToken)
            if user:
                if user == profile:

                    with open("templates/profile.html") as f:
                        returnhtml = f.read()
                else:
                    with open("templates/otherProfile.html") as f:
                        returnhtml = f.read()
                returnhtml = returnhtml.replace("{{user}}", profile)

                # get picture
                filename = get_path(profile)
                print()
                if filename != None:
                    s = 'src="' + filename + '"'
                    returnhtml = returnhtml.replace("{{filename}}", s)
                return returnhtml
                
            else:
                return "auth token doesn't match"
        else:
            return "not logged in"
    else:
        return "not a valid profile"

    


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        form = request.form 
        name = sanitize_data(form["usernameField"])
        password = sanitize_data(form["passwordField"])
        auth_token_resp = auth_token(name, password)
        if auth_token_resp[0]:
            s = url_for("profile", profile=name)

            response = make_response(redirect(s))
            response.set_cookie('auth', auth_token_resp[1])
            return response
            
        else:
            return "wrong credentials"
    else:
        with open("templates/Login.html") as f:
            return f.read()
    return redirect(url_for("root"))


def sanitize_data(data: str) -> str:
    return data.replace(">", "&gt;").replace("<", "&lt;").replace("&","&amp;")

    
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
        print(form, flush=True)
        print("DICT", form.to_dict, type( form.to_dict),flush=True)
        name = sanitize_data(form["usernameField"])
        password = sanitize_data(form["passwordField"])
        print(f"username: {name}, password: {password}", flush=True)
        if create(name, password):
            return redirect(url_for("login"))
        else:
            return "Username exists, choose another one, bitch"
    else:
        with open("templates/Register.html") as f:
            return f.read()

def check_allowed(input: str) -> bool:
    extensions = {'jpg', 'png', 'jpeg'}
    print(f"check_allowed input {input}", flush=True)
    file_type = input.split('.')[1].lower()
    return file_type in extensions

@app.route("/upload/<profile>", methods=["POST","GET"])
def upload(profile):
    if (request.method == "GET"):
        with open("templates/upload_image.html") as f:
            return f.read()
    elif (request.method == "POST"):
        file = request.files['file']
        input_name = file.filename
        if input_name == '':
            return "no file selected, you dumbass >:("
        print(f"input_name:{input_name}",flush=True)
        extension_type = input_name.split(".")[1]
        if not check_allowed(input_name):
            return f"Wrong file type uploaded, <br/>Allowed file type are: jpg, png, and jpeg <br/>The uploaded file type is: {extension_type}"
        filename = "picture" + get_id() + "." + str(extension_type)
        authToken = request.cookies.get('auth')
        user = username_from_auth_token(authToken)
        picture_location(user, filename)
        print("this is the filename", filename,flush=True)
        s = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(s)
        return redirect(url_for("profile", profile=profile)) 
    
@app.route("/images/<image>", methods=["GET"])
def getImage(image):

    return pic_bytes(image)



if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
