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
print("\nUsers:")
if rows:
    for row in rows:
        print(row)
else:
    print("No users found")

# Look at places
cursor.execute("SELECT id, title, description, price, owner_id FROM places;")
rows = cursor.fetchall()
print("\nPlaces:")
if rows:
    for row in rows:
        print(row)
else:
    print("No places found")

# Look at place details
cursor.execute("""
    SELECT p.title, p.description, p.price, p.latitude, p.longitude,
           u.first_name || ' ' || u.last_name AS owner, u.email
    FROM places p
    JOIN users u ON p.owner_id = u.id;
""")
rows = cursor.fetchall()
print("\nPlace Details (with owner):")
if rows:
    for row in rows:
        print(row)
else:
    print("No place details found")

# Look at amenities
cursor.execute("SELECT * FROM amenities;")
rows = cursor.fetchall()
print("\nAmenities:")
if rows:
    for row in rows:
        print(row)
else:
    print("No amenities found")


# Look at reviews
cursor.execute("""
    SELECT r.id, r.text, r.rating, u.email, p.title
    FROM reviews r
    JOIN users u ON r.user_id = u.id
    JOIN places p ON r.place_id = p.id;
""")
rows = cursor.fetchall()
print("\nReviews:")
if rows:
    for row in rows:
        print(row)
else:
    print("No reviews found")


conn.close()
