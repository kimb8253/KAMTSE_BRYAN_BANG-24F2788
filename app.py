from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# Dashboard
@app.route('/')
def dashboard():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT AVG(score) FROM grades")
    avg = c.fetchone()[0]
    if avg is None:
        avg = 0
    c.execute("SELECT subject, AVG(score) FROM grades GROUP BY subject")
    subjects = c.fetchall()
    c.execute("SELECT * FROM grades")
    grades = c.fetchall()
    c.execute("SELECT * FROM revision")
    revision = c.fetchall()
    conn.close()
    return render_template('dashboard.html',
                           avg_grade=round(avg,2),
                           subjects=subjects,
                           grades=grades,
                           revision=revision,
                           date=datetime.date.today().strftime("%B %d, %Y"))

# Grades CRUD
@app.route('/grades', methods=['GET','POST'])
def grades_page():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        score = int(request.form['score'])
        exam_date = request.form['exam_date']
        c.execute("INSERT INTO grades (subject, score, exam_date) VALUES (?,?,?)",
                  (subject, score, exam_date))
        conn.commit()
    c.execute("SELECT * FROM grades")
    grades = c.fetchall()
    conn.close()
    return render_template('grades.html', grades=grades)

@app.route('/edit_grade/<int:id>', methods=['GET','POST'])
def edit_grade(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        score = int(request.form['score'])
        exam_date = request.form['exam_date']
        c.execute("UPDATE grades SET subject=?, score=?, exam_date=? WHERE id=?",
                  (subject, score, exam_date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('grades_page'))
    c.execute("SELECT * FROM grades WHERE id=?", (id,))
    grade = c.fetchone()
    conn.close()
    return render_template('edit_grade.html', grade=grade)

@app.route('/delete_grade/<int:id>')
def delete_grade(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM grades WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('grades_page'))

# Revision CRUD
@app.route('/revision', methods=['GET','POST'])
def revision_page():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        time = request.form['time']
        c.execute("INSERT INTO revision (subject, date, time) VALUES (?,?,?)",
                  (subject, date, time))
        conn.commit()
    c.execute("SELECT * FROM revision")
    revision = c.fetchall()
    conn.close()
    return render_template('revision.html', revision=revision)

@app.route('/edit_revision/<int:id>', methods=['GET','POST'])
def edit_revision(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    if request.method == 'POST':
        subject = request.form['subject']
        date = request.form['date']
        time = request.form['time']
        c.execute("UPDATE revision SET subject=?, date=?, time=? WHERE id=?",
                  (subject, date, time, id))
        conn.commit()
        conn.close()
        return redirect(url_for('revision_page'))
    c.execute("SELECT * FROM revision WHERE id=?", (id,))
    rev = c.fetchone()
    conn.close()
    return render_template('edit_revision.html', rev=rev)

@app.route('/delete_revision/<int:id>')
def delete_revision(id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("DELETE FROM revision WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('revision_page'))

if __name__ == '__main__':
    app.run(debug=True)

