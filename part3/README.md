# HBnB - Part 2: RESTful API

This part implements the Business Logic and Presentation layers as a RESTful API using Flask and Flask-RESTx.

---

## 📁 Contents

### ⚙️ Setup

1. Clone the repository
```bash
git clone https://github.com/TheKasman/holberton-hbnb.git
cd holberton-hbnb/part2
```

2. Install the required packages:
```bash
pip3 install -r requirements.txt
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

### 🔀 API Endpoints

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

### 🧠 Business Logic Layer

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

### 🧪 Testing

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

The examples below are drawn from our black-box testing reports. Start the server with `python3 run.py` before running any command.

*Users*

Create a user — expected `201 Created`:
```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```
```json
{
  "id": "322b1710-0c3d-409a-9e68-22e5fe5013ec",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

*Amenities*

Create an amenity — expected `201 Created`:
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```
```json
{
  "id": "a0ed107c-be43-4375-a4ae-0c07cb1f5ab6",
  "name": "Wi-Fi",
  "created_at": "2026-03-09T03:19:27.428888",
  "updated_at": "2026-03-09T03:19:27.428893"
}
```

*Places*

Create a place — expected `201 Created` (requires a valid `owner_id` from a created user):
```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Beach House", "description": "Nice place", "price": 100, "latitude": 10, "longitude": 20, "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"}'
```
```json
{
  "id": "91ba90de-ab00-44b9-8159-2293aced8c6d",
  "title": "Beach House",
  "description": "Nice place",
  "price": 100,
  "latitude": 10,
  "longitude": 20,
  "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
}
```

*Reviews*

Create a review — expected `201 Created`:
```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing experience!", "rating": 5, "user_id": "user123", "place_id": "place456"}'
```
```json
{
  "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
  "text": "Amazing experience!",
  "rating": 5,
  "user_id": "user123",
  "place_id": "place456"
}
```

---

## 🎯 Objectives

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
