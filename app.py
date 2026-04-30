from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT AVG(score) AS avg_score FROM grades")
    avg_grade = cur.fetchone()["avg_score"]

    cur.execute("SELECT COUNT(DISTINCT subject) AS subject_count FROM grades")
    subject_count = cur.fetchone()["subject_count"]

    cur.execute("SELECT COUNT(*) AS revision_count FROM revisions")
    revision_count = cur.fetchone()["revision_count"]

    cur.execute("SELECT * FROM grades")
    grades = cur.fetchall()

    cur.execute("SELECT * FROM revisions")
    revisions = cur.fetchall()

    conn.close()
    progress = int(avg_grade) if avg_grade else 0

    return render_template(
        'dashboard.html',
        avg_grade=avg_grade,
        subject_count=subject_count,
        revision_count=revision_count,
        grades=grades,
        revisions=revisions,
        progress=progress
    )

# Grades CRUD
@app.route('/grades', methods=['GET', 'POST'])
def grades():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        score = request.form['score']
        cur.execute("INSERT INTO grades (subject, score) VALUES (?, ?)", (subject, score))
        conn.commit()
    cur.execute("SELECT * FROM grades")
    grades = cur.fetchall()
    conn.close()
    return render_template('grades.html', grades=grades)

@app.route('/edit_grade/<int:id>', methods=['GET', 'POST'])
def edit_grade(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM grades WHERE id = ?", (id,))
    grade = cur.fetchone()
    if request.method == 'POST':
        subject = request.form['subject']
        score = request.form['score']
        cur.execute("UPDATE grades SET subject = ?, score = ? WHERE id = ?", (subject, score, id))
        conn.commit()
        conn.close()
        return redirect(url_for('grades'))
    conn.close()
    return render_template('edit_grade.html', grade=grade)

@app.route('/delete_grade/<int:id>', methods=['GET', 'POST'])
def delete_grade(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM grades WHERE id = ?", (id,))
    grade = cur.fetchone()
    if request.method == 'POST':
        cur.execute("DELETE FROM grades WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('grades'))
    conn.close()
    return render_template('delete_grade.html', grade=grade)

# Revisions CRUD
@app.route('/revisions', methods=['GET', 'POST'])
def revisions():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        time = request.form['time']
        cur.execute("INSERT INTO revisions (subject, date, time) VALUES (?, ?, ?)", (subject, date, time))
        conn.commit()
    cur.execute("SELECT * FROM revisions")
    revisions = cur.fetchall()
    conn.close()
    return render_template('revisions.html', revisions=revisions)

@app.route('/edit_revision/<int:id>', methods=['GET', 'POST'])
def edit_revision(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM revisions WHERE id = ?", (id,))
    revision = cur.fetchone()
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        time = request.form['time']
        cur.execute("UPDATE revisions SET subject = ?, date = ?, time = ? WHERE id = ?", (subject, date, time, id))
        conn.commit()
        conn.close()
        return redirect(url_for('revisions'))
    conn.close()
    return render_template('edit_revision.html', revision=revision)

@app.route('/delete_revision/<int:id>', methods=['GET', 'POST'])
def delete_revision(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM revisions WHERE id = ?", (id,))
    revision = cur.fetchone()
    if request.method == 'POST':
        cur.execute("DELETE FROM revisions WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('revisions'))
    conn.close()
    return render_template('delete_revision.html', revision=revision)

if __name__ == '__main__':
    app.run(debug=True)

