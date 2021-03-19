from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
clients = 0
message = ""

@socketio.on('connect')
def connect():
    global clients
    clients += 1
    emit("users", {"user_count": clients, "message" : message}, broadcast = True)

@socketio.on('disconnect')
def disconnect():
    global clients
    clients -=1
    emit("users", {"user_count": clients, "message" : message}, broadcast= True)


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    global message
    message = msg
    send(msg, broadcast=True) #broadcasting received message to all connect clients, including the one that sent it.

if __name__ == '__main__':
    socketio.run(app, debug=True)

