@app.route("/courses")
def courses():
    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("SELECT title, description FROM courses")
    data = c.fetchall()

    conn.close()

    return render_template("courses.html", courses=data)
