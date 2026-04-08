from app import create_app
from app.extensions import db
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

app = create_app()


REVIEWS = [
    {
        "text": "Super affordable and clean, perfect for a short stay!",
        "rating": 4,
        "place_title": "Cheap Studio",
        "reviewer_email": "jane.smith@example.com"
    },
    {
        "text": "Absolutely breathtaking views, worth every penny.",
        "rating": 5,
        "place_title": "Luxury Penthouse",
        "reviewer_email": "jane.smith@example.com"
    },
    {
        "text": "Beautiful and spacious, loved the modern touches.",
        "rating": 5,
        "place_title": "Big Wow Beautiful Apartment",
        "reviewer_email": "jane.smith@example.com"
    },
    {
        "text": "Great location, comfortable and good value.",
        "rating": 4,
        "place_title": "Mid-Range Flat",
        "reviewer_email": "admin@example.com"
    },
    {
        "text": "Clean, central and exactly as described.",
        "rating": 4,
        "place_title": "Mid-Range Flat",
        "reviewer_email": "jane.smith@example.com"
    },
    {
        "text": "Loved the architecture and the shaded balcony — very relaxing.",
        "rating": 5,
        "place_title": "Desert Oasis Retreat",
        "reviewer_email": "jane.smith@example.com"
    },
    {
        "text": "Waking up among the treetops was unforgettable.",
        "rating": 4,
        "place_title": "Canopy Treehouse",
        "reviewer_email": "jane.smith@example.com"
    },
    {
        "text": "The glass windows and ocean views blew me away.",
        "rating": 5,
        "place_title": "Coastal Modern Villa",
        "reviewer_email": "john.doe@example.com"
    },
    {
        "text": "Felt like stepping into a painting, loved every moment.",
        "rating": 4,
        "place_title": "Blossom Lantern House",
        "reviewer_email": "john.doe@example.com"
    },
]

with app.app_context():

    for data in REVIEWS:

        # Resolve place
        place = Place.query.filter_by(title=data["place_title"]).first()
        if not place:
            print(f"Place not found: {data['place_title']} — skipping")
            continue

        # Resolve reviewer
        reviewer = User.query.filter_by(email=data["reviewer_email"]).first()
        if not reviewer:
            print(f"Reviewer not found: {data['reviewer_email']} — skipping")
            continue

        # Skip if this user already reviewed this place
        existing = Review.query.filter_by(
            place_id=place.id,
            user_id=reviewer.id
        ).first()
        if existing:
            print(f"Skipping (already exists): {reviewer.email} → {place.title}")
            continue

        review = Review(
            text=data["text"],
            rating=data["rating"],
            place_id=place.id,
            user_id=reviewer.id
        )

        db.session.add(review)
        print(f"Created review: {reviewer.email} → {place.title}")

    db.session.commit()
    print("\nSeeding complete")