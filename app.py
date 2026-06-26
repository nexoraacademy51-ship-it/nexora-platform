from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "nexora_secret_key"


# ==========================
# DATABASE
# ==========================
def init_db():
    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT
    )
    """)

    c.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        ("admin", "admin123", "admin")
    )

    conn.commit()
    conn.close()


init_db()


# ==========================
# HOME
# ==========================
@app.route("/")
def home():
    return render_template("index.html")# ==========================
# LOGIN
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("nexora.db")
        c = conn.cursor()

        c.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username

            if user[0] == "admin":
                return redirect("/admin")

            return redirect("/")

        return "Invalid username or password"

    return render_template("login.html")


# ==========================
# REGISTER
# ==========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("nexora.db")
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users(username,password,role) VALUES(?,?,?)",
                (username, password, "user")
            )
            conn.commit()
        except:
            conn.close()
            return "Username already exists"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


# ==========================
# LOGOUT
# ==========================
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")# ==========================
# ADMIN
# ==========================
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("SELECT role FROM users WHERE username=?", (session["user"],))
    user = c.fetchone()

    conn.close()

    if not user or user[0] != "admin":
        return "Access Denied"

    return render_template("admin.html")


# ==========================
# DASHBOARD
# ==========================
@app.route("/admin/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    users_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM courses")
    courses_count = c.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        users=users_count,
        courses=courses_count
    )


# ==========================
# COURSES
# ==========================
@app.route("/courses")
def courses():
    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("SELECT title, description FROM courses")
    data = c.fetchall()

    conn.close()

    return render_template("courses.html", courses=data)


# ==========================
# ADD COURSE
# ==========================
@app.route("/admin/add-course", methods=["GET", "POST"])
def add_course():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        conn = sqlite3.connect("nexora.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO courses(title, description) VALUES(?, ?)",
            (title, description)
        )

        conn.commit()
        conn.close()

        return redirect("/admin/dashboard")

    return render_template("add_course.html")


# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
