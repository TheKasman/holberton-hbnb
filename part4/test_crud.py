"""CRUD TESTING ALL THE TABLES"""
import sqlite3
import uuid

# Connect to the database
conn = sqlite3.connect('hbnb.db')
cursor = conn.cursor()

# Helper function to print a table's contents
def show_table(table):
    """Performs SELECT * FROM on specified table"""
    cursor.execute(f"SELECT * FROM {table};")
    rows = cursor.fetchall()
    if rows:
        print(f"Table '{table}':")
        for r in rows:
            print("  ", r)
    else:
        print(f"Table '{table}' is empty.")
    print("-" * 50)

print("\n=== INITIAL DATA ===")
show_table("User")
show_table("Amenity")
show_table("Place")
show_table("Review")
show_table("Place_Amenity")

#======================
#  U S E R   C R U D  |
#======================

print("\n=== USER CRUD TEST ===")

# CREATE
cursor.execute("""
INSERT INTO User (id, first_name, last_name, email, password, is_admin)
VALUES ('test-user-id', 'Test', 'User', 'test@hbnb.io', 'fake_hash', 0)
""")
conn.commit()

# READ
show_table("User")

# UPDATE
cursor.execute("UPDATE User SET first_name='Updated' WHERE id='test-user-id';")
conn.commit()
show_table("User")

# DELETE
cursor.execute("DELETE FROM User WHERE id='test-user-id';")
conn.commit()
show_table("User")

#============================
#  A M E N I T Y   C R U D  |
#============================

print("\n=== AMENITY CRUD TEST ===")

#  CREATE
cursor.execute("INSERT INTO Amenity (id, name) VALUES ('test-amenity-id', 'Test Amenity');")
conn.commit()

#  READ
show_table("Amenity")

#  UPDATE
cursor.execute("UPDATE Amenity SET name='Updated Amenity' WHERE id='test-amenity-id';")
conn.commit()
show_table("Amenity")

#  DELETE
cursor.execute("DELETE FROM Amenity WHERE id='test-amenity-id';")
conn.commit()
show_table("Amenity")

#========================
#  P L A C E   C R U D  |
#========================

print("\n=== PLACE CRUD TEST ===")

#  CREATE
owner_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'  # admin user from seeds
cursor.execute("""
INSERT INTO Place (id, owner_id, title, description)
VALUES ('test-place-id', ?, 'Test Place', 'A cozy test place');
""", (owner_id,))
conn.commit()

#  READ
show_table("Place")

#  UPDATE
cursor.execute("UPDATE Place SET title='Updated Place' WHERE id='test-place-id';")
conn.commit()
show_table("Place")

#  DELETE
cursor.execute("DELETE FROM Place WHERE id='test-place-id';")
conn.commit()
show_table("Place")

#==========================
#  R E V I E W   C R U D  |
#==========================

print("\n=== REVIEW CRUD TEST ===")
# Use the seeded admin user
user_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'

# Insert a temporary place for review testing
place_id = str(uuid.uuid4())
cursor.execute("""
INSERT INTO Place (id, owner_id, title, description)
VALUES (?, ?, 'Temp Place for Review', 'Temporary place for review test');
""", (place_id, user_id))
conn.commit()

#  CREATE
review_id = str(uuid.uuid4())
cursor.execute("""
INSERT INTO Review (id, user_id, place_id, text)
VALUES (?, ?, ?, 'This is a test review');
""", (review_id, user_id, place_id))
conn.commit()

#  READ
cursor.execute("SELECT * FROM Review;")
print("Review table:", cursor.fetchall())

#  UPDATE
cursor.execute("UPDATE Review SET text=? WHERE id=?", ('Updated review text', review_id))
conn.commit()
show_table("Review")

#  DELETE
cursor.execute("DELETE FROM Review WHERE id=?", (review_id,))
conn.commit()
show_table("Review")

#  CLEAN UP DUMMY REVIEW/PLACE
cursor.execute("DELETE FROM Review WHERE id=?", (review_id,))
cursor.execute("DELETE FROM Place WHERE id=?", (place_id,))
conn.commit()

#========================================
#  P L A C E _ A M E N I T Y   C R U D  |
#========================================

print("\n=== PLACE_AMENITY CRUD TEST ===")

# Dummy place to make a place amenity
owner_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
place_id = str(uuid.uuid4())

cursor.execute("""
INSERT INTO Place (id, owner_id, title, description)
VALUES (?, ?, 'Temp Place 2', 'For Place_Amenity');
""", (place_id, owner_id))
conn.commit()

amenity_id = '6f331ea1-5af3-45d9-a782-d2098a876255'  # WiFi from seeds

#  CREATE
cursor.execute("INSERT INTO Place_Amenity (place_id, amenity_id) VALUES (?, ?)",
                (place_id, amenity_id))
conn.commit()
show_table("Place_Amenity")

# UPDATE
new_amenity_id = '3c28b41b-1add-4956-8431-a099346e36df'  # Swimming Pool
cursor.execute("DELETE FROM Place_Amenity WHERE place_id=? AND amenity_id=?",
                (place_id, amenity_id))
cursor.execute("INSERT INTO Place_Amenity (place_id, amenity_id) VALUES (?, ?)",
                (place_id, new_amenity_id))
conn.commit()
show_table("Place_Amenity")

# DELETE
cursor.execute("DELETE FROM Place_Amenity WHERE place_id=? AND amenity_id=?",
                (place_id, new_amenity_id))
cursor.execute("DELETE FROM Place WHERE id=?", (place_id,))
conn.commit()
show_table("Place_Amenity")

# Close connection
conn.close()
print("\n=== CRUD TEST COMPLETE ===")
