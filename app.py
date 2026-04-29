from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database helper
def get_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def dashboard():
    conn = get_db()
    grades = conn.execute("SELECT * FROM grades").fetchall()
    revisions = conn.execute("SELECT * FROM revisions").fetchall()
    conn.close()
    return render_template("dashboard.html", grades=grades, revisions=revisions)

# ---------------- GRADES ----------------
@app.route("/grades")
def grades():
    conn = get_db()
    grades = conn.execute("SELECT * FROM grades").fetchall()
    conn.close()
    return render_template("grades.html", grades=grades)

@app.route("/add_grade", methods=["POST"])
def add_grade():
    subject = request.form["subject"]
    score = request.form["score"]
    conn = get_db()
    conn.execute("INSERT INTO grades (subject, score) VALUES (?, ?)", (subject, score))
    conn.commit()
    conn.close()
    return redirect(url_for("grades"))

@app.route("/delete_grade/<int:id>")
def delete_grade(id):
    conn = get_db()
    conn.execute("DELETE FROM grades WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("grades"))

@app.route("/edit_grade/<int:id>", methods=["GET", "POST"])
def edit_grade(id):
    conn = get_db()
    if request.method == "POST":
        subject = request.form["subject"]
        score = request.form["score"]
        conn.execute("UPDATE grades SET subject=?, score=? WHERE id=?", (subject, score, id))
        conn.commit()
        conn.close()
        return redirect(url_for("grades"))
    grade = conn.execute("SELECT * FROM grades WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_grade.html", grade=grade)

# ---------------- REVISIONS ----------------
@app.route("/revisions")
def revisions():
    conn = get_db()
    revisions = conn.execute("SELECT * FROM revisions").fetchall()
    conn.close()
    return render_template("revisions.html", revisions=revisions)

@app.route("/add_revision", methods=["POST"])
def add_revision():
    subject = request.form["subject"]
    date = request.form["date"]
    time = request.form["time"]
    conn = get_db()
    conn.execute("INSERT INTO revisions (subject, date, time) VALUES (?, ?, ?)", (subject, date, time))
    conn.commit()
    conn.close()
    return redirect(url_for("revisions"))

@app.route("/delete_revision/<int:id>")
def delete_revision(id):
    conn = get_db()
    conn.execute("DELETE FROM revisions WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("revisions"))

@app.route("/edit_revision/<int:id>", methods=["GET", "POST"])
def edit_revision(id):
    conn = get_db()
    if request.method == "POST":
        subject = request.form["subject"]
        date = request.form["date"]
        time = request.form["time"]
        conn.execute("UPDATE revisions SET subject=?, date=?, time=? WHERE id=?", (subject, date, time, id))
        conn.commit()
        conn.close()
        return redirect(url_for("revisions"))
    revision = conn.execute("SELECT * FROM revisions WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit_revision.html", revision=revision)

if __name__ == "__main__":
    app.run(debug=True)

