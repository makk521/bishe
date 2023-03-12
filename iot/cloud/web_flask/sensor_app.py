from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import socket
import sys

"""
Background Thread
"""
thread = None
thread_lock = Lock()
HOST = '10.0.12.13'
ADDR2 = (HOST, 8081)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():

    print("..................Wait for Connection..................")
    sock, address = soc_bg.accept()
    print("Generating random sensor values")
    while True:
        buf = sock.recv(1024)
        data_from_raspberry = eval(buf.decode('utf-8'))
        socketio.emit('updateSensorData', {'value': data_from_raspberry[2], "date": get_current_datetime()})
        socketio.sleep(1)

"""
Serve root index file
"""
@app.route('/')
def index():
    return render_template('index.html')

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    try:
        soc_bg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc_bg.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc_bg.bind(ADDR2)  # 在不同主机或者同一主机的不同系统下使用实际ip
        soc_bg.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    socketio.run(app,host='0.0.0.0', port=5000)
