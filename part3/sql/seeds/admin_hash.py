"""Generate a hash key for admin_user"""
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# The password you want for the admin
password = "admin1234"

# Generate the hash
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
print(hashed_password)