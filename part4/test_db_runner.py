import sqlite3
import glob
import os

# Connect to (or create) the database
db_file = 'development.db'

# Remove old DB to start fresh each run
if os.path.exists(db_file):
    os.remove(db_file)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Function to run all scripts in a folder
def run_scripts(folder):
    sql_files = sorted(glob.glob(f'{folder}/*.sql'))
    for file in sql_files:
        print(f"Running {file}...")
        with open(file, 'r') as f:
            cursor.executescript(f.read())
        print(f"{file} executed successfully!\n")

# Run schema scripts first
run_scripts('sql/schema')

# Then run seed scripts
run_scripts('sql/seeds')

# Show some data for each table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

for table in tables:
    try:
        cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
        rows = cursor.fetchall()
        if rows:
            print(f"Table '{table}' (first 5 rows):")
            for r in rows:
                print(f"  {r}")
        else:
            print(f"Table '{table}' is empty.")
    except Exception as e:
        print(f"Could not query table '{table}': {e}")
    print("-" * 50)

conn.commit()
conn.close()
print("All scripts completed! Database is ready.")