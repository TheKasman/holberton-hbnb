from app import create_app
from app.extensions import db
from app.models.user import User

app = create_app()

USERS = [
    {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "is_admin": False
    },
    {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "password": "jane1234",
        "is_admin": False
    },
]

with app.app_context():

    for data in USERS:
        existing = User.query.filter_by(email=data["email"]).first()
        if existing:
            print(f"Skipping (already exists): {data['email']}")
            continue

        user = User()
        user.set_first_name(data["first_name"])
        user.set_last_name(data["last_name"])
        user.set_email(data["email"])
        user.set_password(data["password"])
        user.is_admin = data["is_admin"]

        db.session.add(user)
        print(f"Created: {data['first_name']} {data['last_name']} ({data['email']})")

    db.session.commit()
    print("\nSeeding complete")