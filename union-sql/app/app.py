from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("db.sqlite3")
    cur = conn.cursor()
    
    # 기존 테이블 제거 및 재생성
    cur.execute("DROP TABLE IF EXISTS products;")
    cur.execute("DROP TABLE IF EXISTS flag;")
    
    # products 테이블
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT);")
    cur.execute("INSERT INTO products (name) VALUES ('Apple'), ('Banana'), ('Carrot');")
    
    # flag 테이블
    cur.execute("CREATE TABLE flag (flag TEXT);")
    cur.execute("INSERT INTO flag (flag) VALUES ('FLAG{union_sql_mastery}');")
    
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        conn = sqlite3.connect("db.sqlite3")
        cur = conn.cursor()
        
        # 취약한 쿼리 - UNION SQLi 유도
        query = f"SELECT id, name FROM products WHERE name LIKE '%{keyword}%'"
        print("[DEBUG]", query)
        try:
            cur.execute(query)
            results = cur.fetchall()
        except:
            results = [("Error", "Invalid Query")]
        conn.close()
    return render_template("index.html", results=results)

@app.route("/flag")
def flag():
    return open("flag.txt").read() if os.path.exists("flag.txt") else "flag.txt not found."

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5002)
