from app import create_app
from app.extensions import db
from app.models.place import Place
from app.models.amenity import Amenity

app = create_app()

with app.app_context():

    # Step 1: Create sample amenities (if not existing)
    amenity_names = ["WiFi", "Pool", "Parking", "Kitchen", "Air Conditioning"]

    amenities = []
    for name in amenity_names:
        existing = Amenity.query.filter_by(name=name).first()
        if not existing:
            new = Amenity(name=name)
            db.session.add(new)
            amenities.append(new)
        else:
            amenities.append(existing)

    db.session.commit()

    # Step 2: Assign amenities to all places
    places = Place.query.all()

    for place in places:
        place.amenities = amenities  # assign all amenities
        print(f"Assigned amenities to {place.title}")

    db.session.commit()

    print("Seeding complete ✅")


app = create_app()
