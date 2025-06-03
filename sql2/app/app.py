from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

FLAG = open("flag.txt").read().strip()

# 초기 DB 설정 (guest와 admin 모두 추가)
def init_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password INTEGER)")
    cur.execute("DELETE FROM users")
    cur.execute("INSERT INTO users VALUES ('admin', 2)")   # 관리자 계정
    cur.execute("INSERT INTO users VALUES ('guest', 0)")   # 게스트 계정
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = "guest"
        password = request.form.get("password", "")
        
        # 취약한 쿼리 (연산자 우선순위 취약점)
        query = f"SELECT * FROM users WHERE username='guest' AND password={password}"
        
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        try:
            cur.execute(query)
            result = cur.fetchone()
        except Exception as e:
            result = None
        conn.close()

        # admin 계정이 반환되면 플래그 노출
        if result and result[0] == 'admin':
            return f"Welcome admin! Flag: {FLAG}"
        return "Login failed!"

    # 기존 로그인 폼 유지
    return render_template("login.html")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)
