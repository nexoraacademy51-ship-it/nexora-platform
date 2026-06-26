from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "nexora_secret_key"

# =========================
# 🧠 DATABASE SETUP
# =========================
def init_db():
    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')

    # Admin default
    c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
              ("admin", "admin123", "admin"))

    conn.commit()
    conn.close()

init_db()

# =========================
# 🏠 HOME
# =========================
@app.route("/")
def home():
    return render_template("index.html")

# =========================
# 🔐 LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("nexora.db")
        c = conn.cursor()

        c.execute("SELECT role FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()

        conn.close()

        if user:
            session["user"] = username
            role = user[0]
            return redirect("/admin" if role == "admin" else "/")

        return "Login Failed"

    return render_template("login.html")

# =========================
# 📝 REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("nexora.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                      (username, password, "user"))
            conn.commit()
        except:
            return "User already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")

# =========================
# 🎓 COURSES (placeholder)
# =========================
@app.route("/courses")
def courses():
    return "<h1>Courses Page (Coming Soon)</h1>"

# =========================
# 👑 ADMIN
# =========================
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("SELECT role FROM users WHERE username=?",
              (session["user"],))
    user = c.fetchone()

    conn.close()

    if not user or user[0] != "admin":
        return "Access Denied"

    return render_template("admin.html")

# =========================
# 🚪 LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

#
