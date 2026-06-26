from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "nexora_secret_key"

# 🧠 Users database (مؤقتة الآن)
users = {
    "admin": {"password": "admin123", "role": "admin"}
}

# 🏠 Home
@app.route("/")
def home():
    return render_template("index.html")

# 🔐 LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect("/admin" if users[username]["role"] == "admin" else "/")

        return "Login Failed"

    return render_template("login.html")


# 📝 REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists"

        users[username] = {"password": password, "role": "user"}
        return redirect("/login")

    return render_template("register.html")


# 🎓 COURSES (مؤقت)
@app.route("/courses")
def courses():
    return "<h1>Courses Page (Coming Soon)</h1>"


# 👑 ADMIN DASHBOARD
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")

    if users.get(session["user"], {}).get("role") != "admin":
        return "Access Denied"

    return render_template("admin.html")


# 🚪 LOGOUT (اختياري لكن مهم)
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
