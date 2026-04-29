import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

# Add the missing column
c.execute("ALTER TABLE revisions ADD COLUMN time TEXT")

conn.commit()
conn.close()

print("Added 'time' column to revisions table.")

