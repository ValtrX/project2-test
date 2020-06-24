import os
import requests
from dotenv import load_dotenv
load_dotenv('.flaskenv')

from time import localtime, strftime
from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = " this is a secret key "
socketio = SocketIO(app)

# Keep track of Room/channels created (Check for channel name)
ROOMS = ["room1", "room2", "room3"]

# Keep track of users logged (Check for username)
usersLogged = []

@app.route("/")
def index():
    
    if(session.get('username')):
        pass

    else:
        return redirect("/signin")

    return render_template("index.html", rooms=ROOMS, username=session.get('username'))

@app.route("/signin", methods=['GET','POST'])
def signin():
    ''' Save the username on a Flask session 
    after the user submit the sign in form '''

    # Forget any username
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":

        # if username in usersLogged:
        #   return render_template("error.html", message="that username already exists!")                   
        
        usersLogged.append(username)

        session['username'] = username

        print(username)

        # Remember the user session on a cookie if the browser is closed.
        session.permanent = True

        return redirect("/")
    else:
        return render_template("signin.html")

@socketio.on('message')
def message(data):
    msg = data["msg"]
    room = data["room"]
    current_user = session.get('username')
    print(session.get('username'))
    print(usersLogged)
    print(f"{data}")

    send({'msg': msg, 'username': current_user, 'room': room, 'time_stamp': strftime('%b-%d %I:%M%p', localtime())}, room=room, broadcast=True)

@socketio.on('join')
def join(data):
    room = data["room"]
    username = data['username']
    join_room(room)

    if(session.get('username') not in usersLogged):

        usersLogged.append(session.get('username'))

    send({"msg": username + " has joined to: " + room}, room=room, broadcast=True)

@socketio.on('leave')
def leave(data):
    room = data["room"]
    username = data['username']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room, broadcast=True)

@socketio.on('new_room')
def new_room(data):
    room = data["new_room_name"]
    print(room)
    ROOMS.append(data["new_room_name"])
    print(ROOMS)
    join_room(room)
    emit('new room received', data, broadcast=True)


###############################  SUPER IMPORTANT ##################

#@socketio.on('my event') #This is what you Receive from the client
#def handle_my_custom_event(arg1):
#    print('received args: ' + arg1)
#    emit('my response', arg1, broadcast=True) #This is what you SEND to the client

################################ END SUPER IMPORTANT ##################

if __name__ == '__main__':
    socketio.run(app)