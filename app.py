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

    
@app.route("/<name>")
def name(name):
    returnhtml = ""

    if check_user(name):
        if "auth" in request.cookies:
            authToken = request.cookies.get('auth')
            user = username_from_auth_token(authToken)
            if user:
                if user == name:

                    with open("templates/profile.html") as f:
                        returnhtml = f.read()
                    returnhtml = returnhtml.replace("{{user}}", name)

                    # get picture
                    filename = get_path(name)
                    if filename != None:
                        s = 'src="' + filename + '"' + ' alt=""'
                        returnhtml = returnhtml.replace("{{filename}}", name)
                    return returnhtml
                # else: #someone else's profile
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
            s = url_for("name", name=form["usernameField"])

            response = make_response(redirect(s))
            response.set_cookie('auth', auth_token_resp[1])
            return response
            
        else:
            return "wrong credentials"
    else:
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
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/Register.html", "xsrf_token", xsrf_token) # HTML templating - adds xsrf token to form

def check_allowed(input: str) -> bool:
    extensions = {'jpg', 'png', 'jpeg'}
    print(f"check_allowed input {input}", flush=True)
    file_type = input.split('.')[1].lower()
    return file_type in extensions

@app.route("/upload/<name>", methods=["POST","GET"])
def upload(name):
    if (request.method == "GET"):
        xsrf_token = generate_xsrf_token()
        # HTML templating - adds xsrf token to form
        return custom_render_template("templates/upload_image.html", "xsrf_token", xsrf_token)
    elif (request.method == "POST"):
        xsrf_token = request.headers.get('xsrf token') # Obtain xsrf token
        valid_xsrf_token = validate_xsrf_token(xsrf_token) # Check xsrf token against those stored in db
        if valid_xsrf_token:
            file = request.files['file']
            input_name = file.filename
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
            return redirect(url_for("name", name=name)) 
        else:
            return "Invalid XSRF Token :("

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
