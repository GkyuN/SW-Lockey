#!/usr/bin/python3
from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)

try:
    FLAG = open('./flag.txt').read()
except:
    FLAG = '[**FLAG**]'

users = {
    'kim': 'bin12',
    'lee': 'ho33',
    'admin': FLAG  # admin은 로그인할 수 없지만, 세션id로 접속 가능
}

# 세션 값은 순서대로 생성
session_seeds = {
    'kim': 'a123b456c789',
    'lee': 'b123c456d789',
    'admin' : 'c123d456e789'
}

session_storage = {
    'a123b456c789': 'kim',
    'b123c456d789': 'lee',
    'c123d456e789': 'admin'  # 수동으로 넣어야만 접근 가능
}

@app.route('/')
def index():
    session_id = request.cookies.get('sessionid')
    username = session_storage.get(session_id)

    if not username:
        return render_template('index.html')

    if username == 'admin':
        return render_template('index.html', text=f"🎉 Welcome admin! Flag: {FLAG}")
    else:
        return render_template('index.html', username=username,text=username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if username not in users:
        return '<script>alert("User not found");history.go(-1);</script>'
    if users[username] != password:
        return '<script>alert("Wrong password");history.go(-1);</script>'

    if username == 'admin':
        return '<script>alert("Admin login is disabled!");history.go(-1);</script>'

    session_id = session_seeds[username]
    session_storage[session_id] = username

    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('sessionid', session_id)
    return resp
   
@app.route('/notice')
def notice():
    return render_template('notice.html')

if __name__ == '__main__':
    print('[DEBUG] Session storage:', session_storage)
    app.run(host='0.0.0.0', port=5002)
