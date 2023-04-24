from flask import Flask, render_template, request, session, redirect, url_for, flash ,Response
from flask_socketio import SocketIO
from threading import Lock,Thread
from datetime import datetime
import socket
import sys
import sqlite3
import os

"""
Background Thread
"""
thread = None
thread_lock = Lock()
HOST = '10.0.12.13'
ADDR2 = (HOST, 8081)
PORT = 7789     # socket通信端口
BUFSIZ = 1024
ADDR = (HOST, PORT)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
DATABASE = 'data.db'
socketio = SocketIO(app, cors_allowed_origins='*')

# 创建用户表
def create_table():
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.close()

# 保存来自树莓派发送过来的数据
def date_save_rasp(device_id,time_from_rasp,led_status):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO data VALUES(:Id,  :date_time, :device_id, :led_status)",
            {'Id': None,  'date_time': time_from_rasp,  'device_id': device_id,  'led_status': int(led_status)})
    conn.commit()
    c.close()
    conn.close()

# 接收来自树莓派发送过来的数据。同样，需要在单独的线程中一直运行。
def receive_from_rasp():
    while(True):
        print('start')
        buf = sock.recv(BUFSIZ)  # 接收数据
        print('received')
        data_from_raspberry = eval(buf.decode('utf-8'))  # 很重要！经测试只能传输字符串类型，用eval转换成tuple。得到(device_id,time_from_rasp,led_status)
        date_save_rasp(data_from_raspberry[0],data_from_raspberry[1],data_from_raspberry[2])

# 查询数据库最新的一条（行）
def date_check():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    max_id = c.execute("SELECT MAX(ID) FROM data ").fetchone() # max_id = (0,)，注意查询出来的都是tuple类型
    sql = "SELECT * FROM data where ID = %s"%max_id[0]
    c.execute(sql)  
    return c.fetchone()

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
        socketio.emit('updateSensorData', {'led_status':data_from_raspberry[0] ,'fun_status':data_from_raspberry[1],'temperature': data_from_raspberry[2],"humidity":data_from_raspberry[3], "date": get_current_datetime()})
        socketio.sleep(1)

if not os.path.isfile('data.db'):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE data (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_time text, 
        device_id integer,
        led_status integer
        )""")
    conn.commit()
    conn.close()


"""
Serve root index file
"""

@app.route("/index", methods=['GET', "POST"])
def index():     
    return render_template("index.html")

# 注册功能
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 获取表单提交的数据
        username = request.form['username']
        password = request.form['password']
        
        # 在数据库中插入新用户
        conn = sqlite3.connect(DATABASE)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        
        
        return redirect(url_for('login'))
    else:
        return render_template("register.html")

# 登录功能
@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 获取表单提交的数据
        username = request.form['username']
        password = request.form['password']
        
        # 查询用户是否存在
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cur.fetchone()
        conn.close()
        
        if user:
            session['username'] = user[0]
            
            return render_template("index.html")
        else:
            flash('用户名或密码错误！')
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

# 查看最新的亮灯时间
@app.route("/message", methods=['GET', "POST"])
def message():
    new = date_check()
    if new[3] == 1:
        led_status = 'on'
    else:
        led_status = 'off'
    
    return render_template("message.html",led_on_time= new[1],led_status = led_status)

@app.route("/control", methods=['GET', "POST"])
def control():
    if request.method == "GET":
        return render_template("control.html")
    else:
        try:
            led_status_control = request.form.get("led_status_control")  # 在网页表单上获取led_status_control
            sock.send(led_status_control.encode('utf-8'))                # 将获取的状态值发到树莓派
        except AttributeError:
            fun_status_control = request.form.get("fun_status_control")  # 在网页表单上获取led_status_control
            sock.send(fun_status_control.encode('utf-8'))        
        print('指令已发送')
        return render_template("control.html")


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
    create_table()
    try:
        soc_bg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc_bg.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc_bg.bind(ADDR2)  # 在不同主机或者同一主机的不同系统下使用实际ip
        soc_bg.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(ADDR)  # 在不同主机或者同一主机的不同系统下使用实际ip
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    sock, addr = s.accept()

    Thread(target = receive_from_rasp).start()

    socketio.run(app,host='0.0.0.0', port=5000)
