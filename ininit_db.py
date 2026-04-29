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

conn.commit()
conn.close()

print("Database initialized with grades and revisions tables.")

