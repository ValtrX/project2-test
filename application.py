import os
import requests
from dotenv import load_dotenv
load_dotenv('.flaskenv')

from time import localtime, strftime
from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
ROOMS = ["room1", "room2", "room3"]

@app.route("/")
def index():
    return render_template("index.html", rooms=ROOMS)

@socketio.on('message')
def message(data):
    msg = data["msg"]
    room = data["room"]
    print(f"{data}")

    send({'msg': msg, 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=room, broadcast=True)

@socketio.on('join')
def join(data):
    room = data["room"]
    join_room(room)
    send({"msg": "someone has joined to: " + room}, room=room, broadcast=True)

@socketio.on('leave')
def leave(data):
    room = data["room"]
    leave_room(room)
    send({"msg": "someone has left"}, room=room)

@socketio.on('new_room')
def new_room(data):
    room = data["new_room_name"]
    print(room)
    ROOMS.append(data["new_room_name"])
    join_room(data['new_room_name'])
    emit('new room received', data, room, broadcast=True)


###############################  SUPER IMPORTANT ##################

#@socketio.on('my event') #This is what you Receive from the client
#def handle_my_custom_event(arg1):
#    print('received args: ' + arg1)
#    emit('my response', arg1, broadcast=True) #This is what you SEND to the client

################################ END SUPER IMPORTANT ##################

if __name__ == '__main__':
    socketio.run(app)