
from flask import Flask, make_response, request, redirect
import os
from save_picture import *
from authentication import *
from logout import *
from authentication import *
from xsrf_tokens import custom_render_template, generate_xsrf_token, validate_xsrf_token
from Template import *

from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import join_room


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './images'

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route("/", methods=["POST", "GET"])
def root():
    print("enters route", flush=True)
    
    if "auth" not in request.cookies:
        return '<div><h1>not logged in</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
    
    authToken = request.cookies.get('auth')
    user = username_from_auth_token(authToken)
    if user == None:
        return '<div><h1>not logged in</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
    template =  open("templates/index.html").read() 
    online = online_now()
    
    
    loop_content = "<h3>Users online:</h3> <ul>"
    for i in online:
        if i != user:
            loop_content += f'<a href="/{i}"><li>' + sanitize_data(i) + '</li></a>'
        

    loop_content += "</ul>"
    loop_start_tag = "{{loop}}"
    loop_end_tag = "{{end_loop}}"

    start_index = template.find(loop_start_tag)
    end_index = template.find(loop_end_tag)

    content = (
            template[:start_index]
            + loop_content
            + template[end_index + len(loop_end_tag) :]
        )
    final_content = content.replace("{{user}}", user)

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
                if sanitize_data(user) == profile:
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
                return '<div><h1>Not Logged in</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
        else:
            return '<div><h1>no user found</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
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
                response = make_response(redirect('/'+form["usernameField"]))
                response.set_cookie('auth', auth_token_resp[1])
                return response
                
            else:
                return '<div><h1>Invalid credentials</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
                
        else:
            return '<div><h1>Invalid xsrf token</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
    else:
        # Populate xsrf token in form
        xsrf_token = generate_xsrf_token()
        return custom_render_template("templates/Login.html", "xsrf_token", xsrf_token) # HTML templating - adds xsrf token to form

    return redirect("/root")

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
                return redirect("/login")
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
            return redirect('/'+profile) 
        else:
            return "Invalid XSRF Token :("

@app.route("/images/<image>", methods=["GET"])
def getImage(image):

    return pic_bytes(image)

localStorage= []
idCounter= [0]
roomTreacker= [""]
onhave=[True]
roomDataBase=[]
@app.route('/chat', methods=[ "GET"])
def flaskSocketio():
    
    if "auth" not in request.cookies:
        return '<div><h1>not logged in</h1><a href="/login">login</a></br><a href="/register">register</a></div>'
    
    authToken = request.cookies.get('auth')
    user = username_from_auth_token(authToken)
    if user == None:
        return '<div><h1>not logged in</h1><a href="/login">login</a></br><a href="/register">register</a></div>'

    return open("templates/ss.html").read()

@socketio.on('handleUpVote')
def on_handleUpVote(data):
    for x in localStorage:
        if x["username"] == data['username']:
            roomTreacker[0]= x["room"]
            break
    toJson = {"username" : sanitize_data(data['username']), "tagId": data['tagId']}
    emit('applyUpVote',toJson, to=roomTreacker[0])

@socketio.on('handleDownVote')
def on_handleDownVote(data):
    for x in localStorage:
        if x["username"] == data['username']:
            roomTreacker[0]= x["room"]
            break
    toJson = {"username" : sanitize_data(data['username']), "tagId": data['tagId']}
    emit('applyDownVote',toJson, to=roomTreacker[0])

@socketio.on('handleChat')
def on_handleChat(data):
    for x in localStorage:
        if x["username"] == data['username']:
            roomTreacker[0]= x["room"]
            break
    idCounter[0]+=1
    # print(idCounter , flush= True)
    protectionHtml= str(data['message'])
    protectionHtml= protectionHtml.replace('&','&amp')
    protectionHtml= protectionHtml.replace('<','&lt')
    protectionHtml= protectionHtml.replace('>','&gt')
    toJson = {"username" : sanitize_data(data['username']), "message": protectionHtml,"idchat": idCounter[0]}
    emit('appendMessage',toJson, to=roomTreacker[0])

@socketio.on('join')
def on_join(data):
    onhave[0]=True
    if (len(roomDataBase)==0):
        onhave[0]=False
        roomDataBase.append({data['room']:1})
        username = sanitize_data(data['username'])
        room = data['room']
        join_room(room)
        print(data, flush=True)
        localStorage.append(data)
        print(localStorage, flush=True)
        emit('enterRoom',username + ' has entered the room.', to=room)
    else:
        for x in roomDataBase:
            if data['room'] in x.keys():
                if x[data['room']]==2:
                    onhave[0]=False
                    username = sanitize_data(data['username'])
                    emit('fullRoom', username)
                    break
                    # tell user that it is full
                    pass
                else:
                    onhave[0]=False
                    x[data['room']]+=1
                    username = sanitize_data(data['username'])
                    room = data['room']
                    join_room(room)
                    print(data, flush=True)
                    localStorage.append(data)
                    print(localStorage, flush=True)
                    emit('enterRoom',username + ' has entered the room.', to=room)
                    break
        if onhave[0]==True:
            print("------------------no more of this", flush=True)
            roomDataBase.append({data['room']:1})
            username = sanitize_data(data['username'])
            room = data['room']
            join_room(room)
            print(data, flush=True)
            localStorage.append(data)
            print(localStorage, flush=True)
            emit('enterRoom',username + ' has entered the room.', to=room)
        


if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
