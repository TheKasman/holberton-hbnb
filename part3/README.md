# HBnB - Part 3: Authentication & Database Integration

This part introduces **authentication, authorization, and persistent storage** using SQLAlchemy. The application is upgraded from an in-memory prototype to a **secure, database-backed API** ready for real-world deployment.

---

## 📁 Contents

### ⚙️ Setup

1. Clone the repository

```bash
git clone https://github.com/TheKasman/holberton-hbnb.git
cd holberton-hbnb/part3
```

2. Install the required packages:

```bash
pip3 install -r requirements.txt
```

The `requirements.txt` file contains:

```
flask
flask-restx
flask-jwt-extended
sqlalchemy
bcrypt
```

3. Run the application:

```bash
python3 run.py
```

The API will be available at `http://127.0.0.1:5000`.

---

### 🔐 Authentication

This part introduces **JWT-based authentication** using `Flask-JWT-Extended`.

* Users must log in to receive a **JWT token**
* Protected endpoints require a valid token
* Tokens must be included in requests:

```bash
Authorization: Bearer <your_token>
```

---

### 🔀 API Endpoints

Flask-RESTx auto-generates Swagger documentation. Once the app is running, visit:

```
http://127.0.0.1:5000/api/v1/
```

#### 🔑 Authentication — `/api/v1/auth`

| Method | Endpoint             | Description                      |
| ------ | -------------------- | -------------------------------- |
| POST   | `/api/v1/auth/login` | Authenticate user and return JWT |

---

#### 👤 Users — `/api/v1/users`

| Method | Endpoint                  | Description                     |
| ------ | ------------------------- | ------------------------------- |
| POST   | `/api/v1/users/`          | Register a new user             |
| GET    | `/api/v1/users/`          | Retrieve all users (admin only) |
| GET    | `/api/v1/users/<user_id>` | Retrieve a user by ID           |
| PUT    | `/api/v1/users/<user_id>` | Update a user                   |

---

#### 🏠 Places — `/api/v1/places`

| Method | Endpoint                    | Description                          |
| ------ | --------------------------- | ------------------------------------ |
| POST   | `/api/v1/places/`           | Create a place (authenticated users) |
| GET    | `/api/v1/places/`           | Retrieve all places                  |
| GET    | `/api/v1/places/<place_id>` | Retrieve a place by ID               |
| PUT    | `/api/v1/places/<place_id>` | Update a place (owner/admin only)    |

---

#### 🛠️ Amenities — `/api/v1/amenities`

| Method | Endpoint                         | Description                    |
| ------ | -------------------------------- | ------------------------------ |
| POST   | `/api/v1/amenities/`             | Create an amenity (admin only) |
| GET    | `/api/v1/amenities/`             | Retrieve all amenities         |
| GET    | `/api/v1/amenities/<amenity_id>` | Retrieve an amenity            |
| PUT    | `/api/v1/amenities/<amenity_id>` | Update an amenity (admin only) |

---

#### 📝 Reviews — `/api/v1/reviews`

| Method | Endpoint                      | Description          |
| ------ | ----------------------------- | -------------------- |
| POST   | `/api/v1/reviews/`            | Create a review      |
| GET    | `/api/v1/reviews/`            | Retrieve all reviews |
| GET    | `/api/v1/reviews/<review_id>` | Retrieve a review    |
| PUT    | `/api/v1/reviews/<review_id>` | Update a review      |
| DELETE | `/api/v1/reviews/<review_id>` | Delete a review      |

---

## 🧠 Business Logic & Persistence Layer

In Part 3, the application transitions from in-memory storage to a **relational database using SQLAlchemy ORM**.

All entities are now mapped to database tables and persist across sessions.

---

### **User** (`app/models/user.py`)

Represents an authenticated user of the system.

| Attribute    | Type     | Rules               |
| ------------ | -------- | ------------------- |
| `id`         | UUID     | Primary key         |
| `first_name` | String   | Required            |
| `last_name`  | String   | Required            |
| `email`      | String   | Required, unique    |
| `password`   | String   | Hashed using bcrypt |
| `is_admin`   | Boolean  | Default: False      |
| `created_at` | DateTime | Auto-set            |
| `updated_at` | DateTime | Auto-updated        |

---

### **Place** (`app/models/place.py`)

Represents a property listed by a user.

| Attribute     | Type             | Rules            |
| ------------- | ---------------- | ---------------- |
| `id`          | UUID             | Primary key      |
| `title`       | String           | Required         |
| `description` | String           | Optional         |
| `price`       | Float            | Must be positive |
| `latitude`    | Float            | Valid range      |
| `longitude`   | Float            | Valid range      |
| `owner_id`    | ForeignKey(User) | Required         |
| `created_at`  | DateTime         | Auto-set         |
| `updated_at`  | DateTime         | Auto-updated     |

---

### **Review** (`app/models/review.py`)

Represents feedback left by a user.

| Attribute    | Type              | Rules        |
| ------------ | ----------------- | ------------ |
| `id`         | UUID              | Primary key  |
| `text`       | String            | Required     |
| `rating`     | Integer           | 1–5          |
| `user_id`    | ForeignKey(User)  | Required     |
| `place_id`   | ForeignKey(Place) | Required     |
| `created_at` | DateTime          | Auto-set     |
| `updated_at` | DateTime          | Auto-updated |

---

### **Amenity** (`app/models/amenity.py`)

Represents a feature available in a place.

| Attribute    | Type     | Rules        |
| ------------ | -------- | ------------ |
| `id`         | UUID     | Primary key  |
| `name`       | String   | Required     |
| `created_at` | DateTime | Auto-set     |
| `updated_at` | DateTime | Auto-updated |

---

### **Entity Relationships**

```
User ──< Place        (one user owns many places)
User ──< Review       (one user writes many reviews)
Place ──< Review      (one place has many reviews)
Place >──< Amenity    (many-to-many relationship)
```

---

## 🗄️ Database Configuration

### Development

* Uses **SQLite**
* Lightweight and easy to set up

### Production

* Configured for **MySQL**
* Scalable and suitable for real-world deployment

Environment-based configuration ensures smooth transition between environments.

---

## 🔐 Authorization Rules

* Only authenticated users can create/update resources
* Only **owners** can modify their own places/reviews
* Only **admins** can:

  * View all users
  * Manage amenities

---

## 📊 Database Design

The database schema is visualized using **Mermaid.js** ER diagrams, ensuring:

* Clear entity relationships
* Proper normalization
* Scalable structure

---

## 🧪 Testing

1. Install pytest:

```bash
pip3 install pytest
```

2. Run tests:

```bash
cd holberton-hbnb/part3
pytest
```

---

## 🎯 Objectives

**Part 3** enhances the architecture by introducing:

* **Authentication Layer** – JWT-based security
* **Authorization Layer** – Role-based access control
* **Persistence Layer** – SQLAlchemy with SQLite/MySQL

This replaces the in-memory storage from Part 2 and prepares the application for production environments.

---

## 👥 Authors

* Andrew Kasapidis
* Matthew Wirski
* Yongshan Liang
* Patrick Macabulos
