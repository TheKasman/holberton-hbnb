from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.create_all()  # ensure tables exist

    admin_email = "pat@example.com"
    admin = User.query.filter_by(email=admin_email).first()

    if not admin:
        admin = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            is_admin=True
        )
        admin.set_password("patrick")  # hashes the password

        db.session.add(admin)
        db.session.commit()
        print("Admin user created!")
    else:
        print("Admin already exists")