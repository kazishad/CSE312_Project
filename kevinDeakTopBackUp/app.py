from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_socketio import emit
from flask_socketio import join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

localStorageGame= []
idCounterGame= [0]
roomTreackerGame= [""]
allSent=[True]
whoWin=""

@app.route('/game', methods=[ "GET"])
def kevingame():
    return render_template('kevinvideogame.html')
@socketio.on('joinGameRoom')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    myJson = {"username": username, "room": room, "TrunUsed": False, "pick": ""}
    localStorageGame.append(myJson)
    emit('enterGameRoom',username + ' has entered the room.', to=room)
@socketio.on('startgame')
def on_startgame(data):
    for x in localStorageGame:
        if x["username"] == data['username']:
            roomTreackerGame[0]= x["room"]
    emit('genGame', {"username":data['username'] },to=roomTreackerGame[0])
@socketio.on('appendGameData')
def on_appendGameData(data):

    allSent[0]=True
    for x in localStorageGame:
        if x["username"] == data['username']:
            x["TrunUsed"]=True
            x["pick"]=data['pick']
            roomTreackerGame[0]= x["room"]

    for x in localStorageGame:
        # print("-----------------",flush=True)
        # print(data,flush=True)
        # print(x,flush=True)
        if x["TrunUsed"]==False:
            allSent[0]=False
    if (allSent[0] ==True):

        print("-----------------",flush=True)
        print(localStorageGame[0],flush=True)
        print(localStorageGame[1],flush=True)
        if(localStorageGame[0]['pick']=='rock' and localStorageGame[1]['pick']=='paper'):
            whoWin= str(localStorageGame[1]['username'])
        elif(localStorageGame[0]['pick']=='rock' and localStorageGame[1]['pick']=='scissor'):
            whoWin= str(localStorageGame[0]['username'])
        elif(localStorageGame[0]['pick']=='rock' and localStorageGame[1]['pick']=='rock'):
            whoWin= "Tie"
        elif(localStorageGame[0]['pick']=='paper' and localStorageGame[1]['pick']=='scissor'):
            whoWin= str(localStorageGame[1]['username'])
        elif(localStorageGame[0]['pick']=='paper' and localStorageGame[1]['pick']=='rock'):
            whoWin= str(localStorageGame[0]['username'])
        elif(localStorageGame[0]['pick']=='paper' and localStorageGame[1]['pick']=='paper'):
            whoWin= "Tie"
        elif(localStorageGame[0]['pick']=='scissor' and localStorageGame[1]['pick']=='paper'):
            whoWin= str(localStorageGame[0]['username'])
        elif(localStorageGame[0]['pick']=='scissor' and localStorageGame[1]['pick']=='rock'):
            whoWin= str(localStorageGame[1]['username'])
        else:
            whoWin= "Tie"

        myJson= {"winner":"","losser":"","tie":""}
        if( whoWin=="Tie"):
            myJson["tie"]="both"
        elif (whoWin == localStorageGame[0]['username']):
            myJson["winner"]=localStorageGame[0]['username']
            myJson["losser"]=localStorageGame[1]['username']
        else:
            myJson["winner"]=localStorageGame[1]['username']
            myJson["losser"]=localStorageGame[0]['username']

        print("-a-aa--aa-a--a", flush=True)
        print(myJson)
        emit('gameResultAppend',myJson, to=roomTreackerGame[0])
    else:
        pass



localStorage= []
idCounter= [0]
roomTreacker= [""]
@app.route('/flaskSocketio', methods=[ "GET"])
def flaskSocketio():
    return render_template('ss.html')

@socketio.on('handleUpVote')
def on_handleUpVote(data):
    for x in localStorage:
        if x["username"] == data['username']:
            roomTreacker[0]= x["room"]
            break
    toJson = {"username" : data['username'], "tagId": data['tagId']}
    emit('applyUpVote',toJson, to=roomTreacker[0])

@socketio.on('handleDownVote')
def on_handleDownVote(data):
    for x in localStorage:
        if x["username"] == data['username']:
            roomTreacker[0]= x["room"]
            break
    toJson = {"username" : data['username'], "tagId": data['tagId']}
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
    toJson = {"username" : data['username'], "message": protectionHtml,"idchat": idCounter[0]}
    emit('appendMessage',toJson, to=roomTreacker[0])

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(data, flush=True)
    localStorage.append(data)
    print(localStorage, flush=True)
    emit('enterRoom',username + ' has entered the room.', to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
