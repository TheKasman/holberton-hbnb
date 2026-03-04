# HBnB

This repository contains the deliverables for the HBnB project, an AirBnB-like application built progressively across multiple parts.  
Part 1 focuses on system design, including architecture planning, class modelling, and behavioural analysis through sequence diagrams.
Part 2 implements the Business Logic and Presentation layers as a RESTful API using Flask and Flask-RESTx.

---

## 📁 Repository Contents

### Part 1 - System Design

`/Part1/class_diagrams/`

High‑resolution versions of the class diagrams created for this stage of the project.  
These are provided separately so they can be viewed or edited in full quality.

`Technical_Document.pdf`

A compiled technical document containing:

- High‑level architecture overview
- Package diagram
- Business Logic class diagram
- Sequence diagrams for key interactions
- Explanations of design decisions and system behaviour

This document acts as the blueprint for the HBnB system and demonstrates our understanding of the architecture before implementation.

### Part 2 - RESTful API

#### Setup

1. Clone the repository
```bash
git clone https://github.com/TheKasman/holberton-hbnb.git
cd holberton-hbnb/part2
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

The `requirements.txt` file contains:

```
flask
flask-restx
```

3. Run the application:

```bash
python3 run.py
```

The API will be available at `http://127.0.0.1:5000`.

#### API Endpoints

Flask-RESTx auto-generates Swagger documentation. Once the app is running, visit `http://127.0.0.1:5000/api/v1/` to explore all endpoints interactively.

**Users — `/api/v1/users`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/users/` | Register a new user |
| GET | `/api/v1/users/` | Retrieve all users |
| GET | `/api/v1/users/<user_id>` | Retrieve a user by ID |
| PUT | `/api/v1/users/<user_id>` | Update a user |

**Amenities — `/api/v1/amenities`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/amenities/` | Register a new amenity |
| GET | `/api/v1/amenities/` | Retrieve all amenities |
| GET | `/api/v1/amenities/<amenity_id>` | Retrieve an amenity by ID |
| PUT | `/api/v1/amenities/<amenity_id>` | Update an amenity |

**Places — `/api/v1/places`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/places/` | Register a new place |
| GET | `/api/v1/places/` | Retrieve all places |
| GET | `/api/v1/places/<place_id>` | Retrieve a place by ID (includes owner & amenities) |
| PUT | `/api/v1/places/<place_id>` | Update a place |
| GET | `/api/v1/places/<place_id>/reviews` | Retrieve all reviews for a place |

**Reviews — `/api/v1/reviews`**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/reviews/` | Register a new review |
| GET | `/api/v1/reviews/` | Retrieve all reviews |
| GET | `/api/v1/reviews/<review_id>` | Retrieve a review by ID |
| PUT | `/api/v1/reviews/<review_id>` | Update a review |
| DELETE | `/api/v1/reviews/<review_id>` | Delete a review |

#### Business Logic Layer

The Business Logic layer lives in `app/models/` and defines the core entities of the application. All entities inherit from `BaseModel`, which provides shared attributes and behaviour:
- A unique UUID identifier generated at creation
- `created_at` and `updated_at` timestamps
- A `save()` method to refresh the updated timestamp
- An `update(data)` method to bulk-update attributes from a dictionary

**User** (`app/models/user.py`)

Represents a person who can own places and write reviews.

| Attribute | Type | Rules |
|-----------|------|-------|
| `id` | String (UUID) | Auto-generated |
| `first_name` | String | Required, max 50 chars |
| `last_name` | String | Required, max 50 chars |
| `email` | String | Required, unique, valid format |
| `is_admin` | Boolean | Defaults to `False` |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-updated on save |

```python
from app.models.user import User

user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
print(user.id)          # e.g. "3fa85f64-5717-4562-b3fc-2c963f66afa6"
print(user.is_admin)    # False

user.update({"first_name": "Jane"})
print(user.first_name)  # "Jane"
```

**Amenity** (`app/models/amenity.py`)

Represents a feature or facility that can be associated with a place (e.g. Wi-Fi, Parking).

| Attribute | Type | Rules |
|-----------|------|-------|
| `id` | String (UUID) | Auto-generated |
| `name` | String | Required, max 50 chars |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-updated on save |

```python
from app.models.amenity import Amenity

amenity = Amenity(name="Wi-Fi")
print(amenity.name)  # "Wi-Fi"
```

**Place** (`app/models/place.py`)

Represents a property listed for rent. Belongs to a `User` (owner) and can have multiple `Review` and `Amenity` instances.

| Attribute | Type | Rules |
|-----------|------|-------|
| `id` | String (UUID) | Auto-generated |
| `title` | String | Required, max 100 chars |
| `description` | String | Optional |
| `price` | Float | Must be positive |
| `latitude` | Float | Must be between -90.0 and 90.0 |
| `longitude` | Float | Must be between -180.0 and 180.0 |
| `owner` | User | Required, must be a valid User instance |
| `reviews` | List | Managed via `add_review()` |
| `amenities` | List | Managed via `add_amenity()` |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-updated on save |

```python
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

owner = User(first_name="Alice", last_name="Smith", email="alice@example.com")
place = Place(title="Cozy Apartment", description="A nice place to stay",
              price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)

wifi = Amenity(name="Wi-Fi")
place.add_amenity(wifi)
print(len(place.amenities))  # 1

review = Review(text="Loved it!", rating=5, place=place, user=owner)
place.add_review(review)
print(place.reviews[0].text)  # "Loved it!"
```

**Review** (`app/models/review.py`)

Represents feedback left by a `User` about a `Place`. This is the only entity that supports deletion via the API.

| Attribute | Type | Rules |
|-----------|------|-------|
| `id` | String (UUID) | Auto-generated |
| `text` | String | Required |
| `rating` | Integer | Must be between 1 and 5 |
| `place` | Place | Required, must be a valid Place instance |
| `user` | User | Required, must be a valid User instance |
| `created_at` | DateTime | Auto-set on creation |
| `updated_at` | DateTime | Auto-updated on save |

```python
from app.models.review import Review

review = Review(text="Great stay!", rating=5, place=place, user=owner)
print(review.rating)  # 5

review.update({"text": "Amazing stay!", "rating": 4})
print(review.text)    # "Amazing stay!"
```

**Entity Relationships**

```
User ──< Place        (one user can own many places)
User ──< Review       (one user can write many reviews)
Place ──< Review      (one place can have many reviews)
Place >──< Amenity    (many-to-many via a list on Place)
```

All cross-entity references are validated to ensure related objects exist before being linked.

#### Testing

1. Install pytest:

```bash
pip3 install pytest
```

2. Run the tests:

```bash
cd holberton-hbnb/part2
pytest
```

**Manual testing with cURL**

Create a user:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```

Create an amenity:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

Create a place:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": ""}'
```

Create a review:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Great stay!", "rating": 5, "user_id": "", "place_id": ""}'
```

---

## 🎯 Purpose

**Part 1** focuses on planning the system before writing code.  
The goal is to:

- Define the structure of the system
- Model the core entities and their relationships
- Understand how the system behaves through sequence diagrams
- Establish a clear architectural foundation for later development

**Part 2** implements that design as a working API, using the **Facade pattern** to manage communication between three layers:
- **Presentation Layer** - Flask-RESTx API endpoints (`app/api/`)
- **Business Logic Layer** - Entity models with validation (`app/models/`)
- **Persistence Layer** - In-memory repository (`app/persistence/`), to be replaced by SQLAlchemy in Part 3

---

## 👥 Authors
- Andrew Kasapidis
- Matthew Wirski
- Yongshan Liang
- Patrick Macabulos
