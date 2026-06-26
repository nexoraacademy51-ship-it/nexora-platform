@app.route("/admin/dashboard")
def admin_dashboard():
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("nexora.db")
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users")
    users_count = c.fetchone()[0]

    conn.close()

    return render_template("dashboard.html", users=users_count)
