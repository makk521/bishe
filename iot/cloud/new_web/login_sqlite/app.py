from flask import Flask, render_template, request, session, redirect, url_for, flash ,Response
import sqlite3

app = Flask(__name__)
app.secret_key = "secret-key"

# 定义数据库名称
DATABASE = 'users.db'

# 创建用户表
def create_table():
    conn = sqlite3.connect(DATABASE)
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    conn.close()

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
        
        flash('注册成功！')
        return redirect(url_for('login'))
    else:
        return render_template("register.html")


# 登录功能
@app.route('/login', methods=['GET', 'POST'])
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
            flash('登录成功！')
            return Response('<p>登陆成功</p> ')
        else:
            flash('用户名或密码错误！')
            return redirect(url_for('login'))
    else:
        return render_template("login.html")

# 主页
@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return Response('<p>登陆成功</p>')

# 退出登录
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('已退出登录！')
    return Response('<p>退出成功</p>')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)

