from app import create_app
from app.extensions import db
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.user import User

app = create_app()

PLACES = [
    {
        "title": "Cheap Studio",
        "description": "Cozy and affordable",
        "price": 9.0,
        "latitude": 48.8566,
        "longitude": 2.3522,
        "image_url": "/static/images/studio.png",
        "owner_email": "admin@example.com",
        "amenity_names": ["WiFi", "Kitchen"]
    },
    {
        "title": "Mid-Range Flat",
        "description": "Nice central apartment",
        "price": 45.0,
        "latitude": 48.86,
        "longitude": 2.34,
        "image_url": "/static/images/mid_range _flat.png",
        "owner_email": "john.doe@example.com",
        "amenity_names": ["WiFi", "Kitchen", "Parking"]
    },
    {
        "title": "Luxury Penthouse",
        "description": "Stunning rooftop views",
        "price": 250.0,
        "latitude": 48.87,
        "longitude": 2.33,
        "image_url": "/static/images/penthouse.png",
        "owner_email": "admin@example.com",
        "amenity_names": ["WiFi", "Pool", "Parking", "Kitchen", "Air Conditioning"]
    },
    {
        "title": "Big Wow Beautiful Apartment",
        "description": "A big, comfortable and beautiful and modern apartment in the city center.",
        "price": 120.0,
        "latitude": 58.87,
        "longitude": 2.33,
        "image_url": "/static/images/apartment.png",
        "owner_email": "admin@example.com",
        "amenity_names": ["WiFi", "Pool", "Kitchen", "Air Conditioning"]
    },
    {
        "title": "Desert Oasis Retreat",
        "description": "Tucked beside a peaceful palm tree, this charming desert retreat offers a warm, cozy escape inspired by Middle Eastern architecture. Featuring intricate tile details, arched doorways, and a shaded balcony, it’s the perfect place to unwind with a cup of tea after a long journey across the dunes.",
        "price": 99.0,
        "latitude": 53.87,
        "longitude": 12.33,
        "image_url": "/static/images/desert_oasis_retreat.png",
        "owner_email": "john.doe@example.com",
        "amenity_names": ["Parking", "Pool", "Kitchen", "Air Conditioning"]
    },
    {
        "title": "Coastal Modern Villa",
        "description": "Modern beachfront villa. With floor-to-ceiling glass windows, an open-plan layout, and a relaxing outdoor lounge by the water, this home is perfect for soaking in sunsets and enjoying a stylish getaway.",
        "price": 200.0,
        "latitude": 28.87,
        "longitude": 22.33,
        "image_url": "/static/images/modern_house.png",
        "owner_email": "jane.smith@example.com",
        "amenity_names": ["WiFi", "Pool", "Kitchen", "Air Conditioning", "Parking"]
    },
    {
        "title": "Blossom Lantern House",
        "description": "Step into a serene cultural escape with this elegant lantern-lit home. Decorated with blooming flowers and classic East Asian architectural elements, this peaceful residence blends tradition and beauty—ideal for a quiet and scenic stay.",
        "price": 130.0,
        "latitude": 88.87,
        "longitude": 32.33,
        "image_url": "/static/images/blossom_lantern_house.png",
        "owner_email": "jane.smith@example.com",
        "amenity_names": ["WiFi", "Kitchen", "Air Conditioning"]
    },
    {
        "title": "Canopy Treehouse",
        "description": "Escape into nature with this breathtaking multi-level treehouse nestled high among lush green canopies.",
        "price": 55.0,
        "latitude": 83.87,
        "longitude": 30.33,
        "image_url": "/static/images/tree_house.png",
        "owner_email": "john.doe@example.com",
        "amenity_names": ["Parking"]
    },
]

with app.app_context():

    # ── 1. Load amenities (seed_amenities.py must have run first) ─────
    amenity_map = {a.name: a for a in Amenity.query.all()}
    if not amenity_map:
        print("No amenities found — run seed_amenities.py first")
        exit(1)
    print(f"Amenities loaded: {list(amenity_map.keys())}")

    # ── 2. Create places ──────────────────────────────────────────────
    for data in PLACES:

        existing = Place.query.filter_by(title=data["title"]).first()
        if existing:
            print(f"Skipping (already exists): {data['title']}")
            continue

        owner = User.query.filter_by(email=data["owner_email"]).first()
        if not owner:
            print(f"Owner not found for '{data['title']}' ({data['owner_email']}) — skipping")
            continue

        place = Place(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            owner_id=owner.id
        )
        place.image_url = data["image_url"]

        place.amenities = [amenity_map[n] for n in data["amenity_names"] if n in amenity_map]

        db.session.add(place)
        print(f"Created: {place.title} → {data['image_url']}")

    db.session.commit()
    print("\nSeeding complete")