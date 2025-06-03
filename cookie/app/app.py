#!/usr/bin/python3
from flask import Flask, request, render_template, make_response, redirect, url_for
import base64

app = Flask(__name__)

try:
    FLAG = open('./app/flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

users = {
    'kim': 'kim99',
    'admin': FLAG
}


@app.route('/')
def index():
    user_raw = request.cookies.get('user')
    if user_raw:
        try:
            username = base64.b64decode(user_raw.encode()).decode()
        except:
    	    return '''
            <div style="margin:50px auto; max-width:400px; padding:20px; 
                border:2px solid #e74c3c; border-radius:8px; 
                color:#e74c3c; font-weight:bold; text-align:center; 
                font-family: Arial, sans-serif;">
        🚫 You put the wrong cookie value! 🚫
    </div>
    '''

        return render_template('index.html', username=username, flag=FLAG if username == 'admin' else None)
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            pw = users[username]
        except:
            return '<script>alert("not found user");history.go(-1);</script>'
        if pw == password:
            resp = make_response(redirect(url_for('index')) )
            user_encoded = base64.b64encode(username.encode()).decode()
            resp.set_cookie('user', user_encoded)
            return resp 
        return '<script>alert("wrong password");history.go(-1);</script>'

app.run(host='0.0.0.0', port=5001)
