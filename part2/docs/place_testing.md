# Place Endpoint Testing Report

## Environment

- Flask app running locally via Docker
- Base URL: http://127.0.0.1:5000
- API Prefix: /api/v1
- Testing tool: cURL
- Swagger UI verified and accessible

---

## How to Reproduce Tests

1.  Start the Flask server:

```
    python3 run.py
```

2.  Run the cURL commands below exactly as written.

---

## 1. Create User -- Valid Case

### Endpoint

POST /api/v1/users/

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    }'

### Expected Result

- HTTP 201 Created
- JSON containing: id, first_name, last_name, email

### Actual Result

Status:

    HTTP/1.1 201 CREATED

Response:

```json
{
  "id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

Result: PASS

---

## 2. Create Place -- Valid Case

### Endpoint

POST /api/v1/places/

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "title": "Beach House",
      "description": "Nice place",
      "price": 100,
      "latitude": 10,
      "longitude": 20,
      "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
    }'

### Expected Result

- HTTP 201 Created
- JSON containing id, title, description, price, latitude, longitude,
  owner_id

### Actual Result

Status:

    HTTP/1.1 201 CREATED

Response:

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

Result: PASS

---

## 3. Create Place -- Missing Required Field (title)

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "price": 100,
      "latitude": 10,
      "longitude": 20,
      "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
    }'

### Actual Result

Status:

    HTTP/1.1 400 BAD REQUEST

Response:

```json
{
  "errors": {
    "title": "'title' is a required property"
  },
  "message": "Input payload validation failed"
}
```

Result: PASS

---

## 4. Create Place -- Invalid Price (Negative Value)

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "title": "Invalid Price",
      "price": -10,
      "latitude": 10,
      "longitude": 20,
      "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
    }'

### Actual Result

Status:

    HTTP/1.1 400 BAD REQUEST

Response:

```json
{
  "error": "Price must be a positive value"
}
```

Result: PASS

---

## 5. Create Place -- Invalid Latitude (Out of Range)

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "title": "Bad Latitude",
      "price": 100,
      "latitude": 100,
      "longitude": 20,
      "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
    }'

### Actual Result

Status:

    HTTP/1.1 400 BAD REQUEST

Response:

```json
{
  "error": "Latitude must be between -90.0 and 90.0"
}
```

Result: PASS

---

## 6. Create Place -- Invalid Longitude (Out of Range)

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "title": "Bad Longitude",
      "price": 100,
      "latitude": 10,
      "longitude": 200,
      "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
    }'

### Actual Result

Status:

    HTTP/1.1 400 BAD REQUEST

Response:

```json
{
  "error": "Longitude must be between -180.0 and 180.0"
}
```

Result: PASS

---

## 7. Create Place -- Invalid Owner

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "title": "Invalid Owner",
      "price": 100,
      "latitude": 10,
      "longitude": 20,
      "owner_id": "nonexistent-id"
    }'

### Actual Result

Status:

    HTTP/1.1 400 BAD REQUEST

Response:

```json
{
  "error": "Owner not found"
}
```

Result: PASS
