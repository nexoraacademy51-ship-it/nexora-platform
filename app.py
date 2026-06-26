from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🚀 Nexora Platform</h1>
    <p>Welcome to Nexora Platform!</p>
    <p>The project is running successfully.</p>
    <p><a href="/admin">Go to Admin Panel</a></p>
    """

@app.route("/admin")
def admin():
    return """
    <h1>👑 Nexora Admin Panel</h1>
    <p>Welcome to Nexora Platform.</p>
    <p>The admin dashboard is under development.</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
