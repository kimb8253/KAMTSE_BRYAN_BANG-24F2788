import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

# Create grades table
c.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL
)
""")

# Create revisions table
c.execute("""
CREATE TABLE IF NOT EXISTS revisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

# Insert sample grades
c.execute("INSERT INTO grades (subject, score) VALUES ('Math', 85)")
c.execute("INSERT INTO grades (subject, score) VALUES ('Physics', 90)")
c.execute("INSERT INTO grades (subject, score) VALUES ('Computer Science', 95)")

# Insert sample revisions
c.execute("INSERT INTO revisions (subject, date) VALUES ('Math', '2026-05-01')")
c.execute("INSERT INTO revisions (subject, date) VALUES ('Physics', '2026-05-03')")
c.execute("INSERT INTO revisions (subject, date) VALUES ('Computer Science', '2026-05-05')")

conn.commit()
conn.close()

print("Database initialized with sample grades and revisions.")
