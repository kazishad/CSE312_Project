from flask import Flask, request
# import Register

app = Flask(__name__)



@app.route("/")
def hello_world():


    with open('Registration/Register.html', 'r') as f:
        html_string = f.read()
    return html_string