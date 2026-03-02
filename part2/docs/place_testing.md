# Place endpoint testing report

## Environment
- Flask app running locally via Docker
- URL: http://127.0.0.1:5000
- Tested using cURL
- Swagger UI verified

---
## 1. Create User – Valid Case

Endpoint:
POST /api/v1/users/

Input:
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}

Expected:
201 Created
JSON containing id, first_name, last_name, email

Actual:
201 Created
Returned:
{
  "id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}

Result:
PASS

## 2. Create Place – Valid Case

Endpoint:
POST /api/v1/places/

Input:
{
  "title": "Beach House",
  "description": "Nice place",
  "price": 100,
  "latitude": 10,
  "longitude": 20,
  "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
}

Expected:
201 Created
JSON containing id, title, description, price, latitude, longitude, owner_id

Actual:
201 Created
Returned:
{
  "id": "91ba90de-ab00-44b9-8159-2293aced8c6d",
  "title": "Beach House",
  "description": "Nice place",
  "price": 100,
  "latitude": 10,
  "longitude": 20,
  "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
}

Result:
PASS

## 3. Create Place – Missing Required Field

Endpoint:
POST /api/v1/places/

Input:
{
  "price": 100,
  "latitude": 10,
  "longitude": 20,
  "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
}

Expected:
400 Bad Request
Validation error for missing required field "title"

Actual:
400 Bad Request
{
  "errors": {
    "title": "'title' is a required property"
  },
  "message": "Input payload validation failed"
}

Result:
PASS

Note:
Validation was handled by Flask-RESTx schema validation before reaching the facade.

## 5. Create Place – Invalid Latitude (Out of Range)

Endpoint:
POST /api/v1/places/

Input:
{
  "title": "Bad Latitude",
  "price": 100,
  "latitude": 100,
  "longitude": 20,
  "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
}

Expected:
400 Bad Request
Error indicating latitude must be between -90 and 90

Actual:
400 Bad Request
{
  "error": "Latitude must be between -90.0 and 90.0"
}

Result:
PASS

## 6. Create Place – Invalid Longitude (Out of Range)

Endpoint:
POST /api/v1/places/

Input:
{
  "title": "Bad Longitude",
  "price": 100,
  "latitude": 10,
  "longitude": 200,
  "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
}

Expected:
400 Bad Request
Error indicating longitude must be between -180 and 180

Actual:
400 Bad Request
{
  "error": "Longitude must be between -180.0 and 180.0"
}

Result:
PASS

## 7. Create Place – Invalid Owner

Endpoint:
POST /api/v1/places/

Input:
{
  "title": "Invalid Owner",
  "price": 100,
  "latitude": 10,
  "longitude": 20,
  "owner_id": "nonexistent-id"
}

Expected:
400 Bad Request
Error indicating owner not found

Actual:
400 Bad Request
{
  "error": "Owner not found"
}

Result:
PASS