from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()  # ensure tables exist

    admins = [
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "password": "password123"
        },
        {
            "first_name": "Admin",
            "last_name": "User",
            "email": "pat@example.com",
            "password": "patrick"
        },
    ]

    for admin_data in admins:
        admin = User.query.filter_by(email=admin_data["email"]).first()
        if not admin:
            admin = User(
                first_name=admin_data["first_name"],
                last_name=admin_data["last_name"],
                email=admin_data["email"],
                is_admin=True
            )
            admin.set_password(admin_data["password"])
            db.session.add(admin)
            print(f"Admin {admin_data['email']} created!")
        else:
            print(f"Admin {admin_data['email']} already exists")

    db.session.commit()