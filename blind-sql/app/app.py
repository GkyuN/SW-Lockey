from flask import Flask, request, render_template
import sqlite3
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT);")
    cur.execute("DELETE FROM users;")
    cur.execute("INSERT INTO users VALUES ('admin', 'bl1ndpass');")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # 🚫 특정 키워드 필터링: 직접적 SQLi 우회 방지
        forbidden_keywords = [ ";", " or ", "OR ", "UNION", "union", "SELECT", "select", "like"]
        for word in forbidden_keywords:
            if word in username.lower() or word in password.lower():
                return "<p>Hacking detected!</p>"

        # 쿼리 실행
        conn = sqlite3.connect("db.sqlite3")
        cur = conn.cursor()

        # SQL 인젝션을 통한 블라인드 인젝션 쿼리: 사용자 입력을 그대로 사용
        query = f"""
        SELECT * FROM users WHERE username = '{username}' AND password = '{password}'
        """

        print("[DEBUG]", query)
        try:
            cur.execute(query)
            result = cur.fetchone()
        except:
            result = None
        conn.close()

        if result:
            return "<p>Access Denied</p>"  # 비밀번호 첫 문자가 맞으면, 접근 거부 메시지
        else:
            return "<p>Invalid login.</p>"  # 비밀번호가 맞지 않으면 Invalid login

    return render_template("index.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5003)
