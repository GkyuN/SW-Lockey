from flask import Flask, request, render_template, make_response
import os

app = Flask(__name__, template_folder='templates')

with open('flag.txt', 'r') as f:
    FLAG = f.read().strip()

@app.route('/')
def index():
    user_flag = request.cookies.get('flag')

    if user_flag is None:
        user_flag = "No flag found. Try to find the flag!"

    return render_template('index.html', flag=user_flag)

@app.route('/set_flag')
def set_flag():
    resp = make_response("Flag has been set in your cookies!")
    resp.set_cookie('flag', FLAG)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
