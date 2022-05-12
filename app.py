import re
from tabnanny import check
from flask import Flask, make_response, render_template, request, redirect, url_for
import os
from save_picture import *
from authentication import *



import db
from xsrf_tokens import custom_render_template, generate_xsrf_token, validate_xsrf_token

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
                    returnhtml = custom_render_template("templates/profile.html", "user", profile)
                else:
                    returnhtml = custom_render_template("templates/otherProfile.html", "user", profile)

                # get picture
                filename = get_path(profile)
                print()
                if filename != None:
                    s = 'src="' + filename + '"'
                    returnhtml = returnhtml.replace("{{filename}}", s)

                # Populate xsrf token in form
                xsrf_token = generate_xsrf_token()
                returnhtml = returnhtml.replace("{{xsrf_token}}", xsrf_token)
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
        auth_token_resp = auth_token(form["usernameField"], form["passwordField"])
        if auth_token_resp[0]:
            s = url_for("profile", profile=form["usernameField"])

            response = make_response(redirect(s))
            response.set_cookie('auth', auth_token_resp[1])
            return response
            
        else:
            return "wrong credentials"
    else:
        # Populate xsrf token in form
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/Login.html", "xsrf_token", xsrf_token) # HTML templating - adds xsrf token to form

@app.route("/register", methods=["POST", "GET"])
def register():

    # with open('static/Register.html', 'r') as f:
    #     html_string = f.read()
    if request.method == "POST":
        form = request.form
        print(form, flush=True)
        print("DICT", form.to_dict, type( form.to_dict),flush=True)
        create(form["usernameField"], form["passwordField"])
        return redirect(url_for("login"))
    else:
        # Populate xsrf token in form
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/Register.html", "xsrf_token", xsrf_token) # HTML templating - adds xsrf token to form

def check_allowed(input: str) -> bool:
    extensions = {'jpg', 'png', 'jpeg'}
    print(f"check_allowed input {input}", flush=True)
    file_type = input.split('.')[1].lower()
    return file_type in extensions

@app.route("/upload/<profile>", methods=["POST","GET"])
def upload(profile):
    if (request.method == "GET"):
        # Populate xsrf token in form
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/upload_image.html", "xsrf_token", xsrf_token)
    elif (request.method == "POST"):
        xsrf_token = request.form["xsrf_token"] # Obtain xsrf token
        print(f"==> xsrf_token (singular) was: {xsrf_token} of type {type(xsrf_token)}", flush=True)
        valid_xsrf_token = validate_xsrf_token(xsrf_token) # Check xsrf token against those stored in db
        if valid_xsrf_token:
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
        else:
            return "Invalid XSRF Token :("

    
@app.route("/images/<image>", methods=["GET"])
def getImage(image):

    return pic_bytes(image)

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
