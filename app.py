import re
from flask import Flask, make_response, request, redirect, url_for
import os
from save_picture import *
from authentication import *
from logout import *
from authentication import *

import db
from xsrf_tokens import custom_render_template, generate_xsrf_token, validate_xsrf_token
from Template import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

@app.route("/", methods=["POST", "GET"])
def root():
    if "auth" not in request.cookies:
        return '<div><h1>not logged in</h1><a href="/login">login</a><a href="/register">register</a></div>'


    template =  open("templates/index.html").read() 
    online = online_now()
    authToken = request.cookies.get('auth')
    user = username_from_auth_token(authToken)
    loop_content = "<h3>Users online:</h3> <ul>"
    for i in online:
        if i != user:
            loop_content += f'<a href="/{i}"><li>' + sanitize_data(i) + '</li></a>'
        

    loop_content += "</ul>"
    loop_start_tag = "{{loop}}"
    loop_end_tag = "{{end_loop}}"

    start_index = template.find(loop_start_tag)
    end_index = template.find(loop_end_tag)

    final_content = (
            template[:start_index]
            + loop_content
            + template[end_index + len(loop_end_tag) :]
        )
    return final_content

    


    
@app.route("/<profile>")
def profile(profile):
    returnhtml = ""
    profile = sanitize_data(profile)
    print(f"profile func {profile}", flush=True)
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

                if filename != None:
                    s = 'src="' + filename + '"'
                    returnhtml = returnhtml.replace("{{filename}}", s)

                # Populate xsrf token in form
                xsrf_token = generate_xsrf_token()
                returnhtml = returnhtml.replace("{{xsrf_token}}", xsrf_token)
                return returnhtml
                
            else:
                return '<div><h1>no user found</h1><a href="/login">login</a><a href="/register">register</a></div>'
        else:
            return '<div><h1>no user found</h1><a href="/login">login</a><a href="/register">register</a></div>'
    else:
        return '<div><h1>Not a valid profile</h1><a href="/">Click here to go to the homepage</a></div>'

    
def sanitize_data(s: str) -> str:
    s = s.replace("&", "&amp;")
    s = s.replace(">", "&gt;")
    s = s.replace("<", "&lt;")

    return s



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        valid_xsrf_token = validate_xsrf_token(request.form["xsrf_token"]) # Check xsrf token against those stored in db
        if valid_xsrf_token:
            form = request.form 
            auth_token_resp = auth_token(form["usernameField"], form["passwordField"])
            if auth_token_resp[0]:
                s = url_for("profile", profile=form["usernameField"])

                response = make_response(redirect(s))
                response.set_cookie('auth', auth_token_resp[1])
                return response
                
            else:
                return '<div><h1>Invalid credentials</h1><a href="/login">login</a><a href="/register">register</a></div>'
                
        else:
            return '<div><h1>Invalid xsrf token</h1><a href="/login">login</a><a href="/register">register</a></div>'
    else:
        # Populate xsrf token in form
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/Login.html", "xsrf_token", xsrf_token) # HTML templating - adds xsrf token to form

    return redirect(url_for("root"))


@app.route("/logout", methods=["POST"])
def logout():
    authToken = request.cookies.get('auth')
    username = username_from_auth_token(authToken)
    if username:
        logout_user(username)
        return '<div><h1>You have been logged out.</h1><a href="/login">log in here.</a><a href="/register">register</a></div>'
    else:
        return '<div><h1>Invalid auth token</h1><a href="/login">log in here.</a></div>'


@app.route("/register", methods=["POST", "GET"])
def register():

    # with open('static/Register.html', 'r') as f:
    #     html_string = f.read()
    if request.method == "POST":
        valid_xsrf_token = validate_xsrf_token(request.form["xsrf_token"]) # Check xsrf token against those stored in db
        if valid_xsrf_token:
            form = request.form
            print(form, flush=True)
            print("DICT", form.to_dict, type( form.to_dict),flush=True)
            if create(form["usernameField"], form["passwordField"]):
                return redirect(url_for("login"))
            else:
                return "Username exists, choose another one, bitch"

        else:
            return "Invalid XSRF Token :("
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
    print(f"profile received {profile}", flush=True)
    if (request.method == "GET"):
        # Populate xsrf token in form
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/upload_image.html", "xsrf_token", xsrf_token)
    elif (request.method == "POST"):
        valid_xsrf_token = validate_xsrf_token(request.form["xsrf_token"]) # Check xsrf token against those stored in db
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
