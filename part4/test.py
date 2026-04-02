import sqlite3

db_path = "development.db"  # adjust to where your DB actually is
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Look at users
cursor.execute("SELECT * FROM users;")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(row)
else:
    print("No users found")

conn.close()
