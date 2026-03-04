# Place Endpoint Testing Report

## Overview
This document logs the manual black-box testing performed on the Place
endpoint of the HBnB REST API. Tests were carried out using cURL against
a locally running Flask development server at http://127.0.0.1:5000.

---

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

`POST /api/v1/users/`

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com"
    }'

### Actual Result

**Status:** HTTP/1.1 201 CREATED

**Response:**

```json
{
  "id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

**Result:** PASS

---

## 2. Create Place -- Valid Case

### Endpoint

`POST /api/v1/places/`

### cURL Command

    curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{
      "title": "Beach House",
      "description": "Nice place",
      "price": 100,
      "latitude": 10,
      "longitude": 20,
      "owner_id": "fd0aa49d-2b75-45cd-9066-89a8c7a07209"
    }'

### Actual Result

**Status:** HTTP/1.1 201 CREATED

**Response:**

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

**Result:** PASS

---

## 3. GET All Places

### Endpoint

`GET /api/v1/places/`

### cURL Command

    curl -i -X GET "http://127.0.0.1:5000/api/v1/places/"

**Result:** PASS

---

## 4. GET Specific Place

### cURL Command

    curl -i -X GET "http://127.0.0.1:5000/api/v1/places/91ba90de-ab00-44b9-8159-2293aced8c6d"

**Result:** PASS

---

## 5. GET Non-Existent Place

### cURL Command

    curl -i -X GET "http://127.0.0.1:5000/api/v1/places/nonexistent-id"

**Status:** HTTP/1.1 404 NOT FOUND

**Response:**

```json
{
  "error": "Place not found"
}
```

**Result:** PASS

---

## 6. PUT Update Place -- Valid Case

### cURL Command

    curl -i -X PUT "http://127.0.0.1:5000/api/v1/places/91ba90de-ab00-44b9-8159-2293aced8c6d" -H "Content-Type: application/json" -d '{
      "price": 180
    }'

Status: HTTP/1.1 200 OK

**Result:** PASS

---

## 7. PUT Update Place -- Validation Bug Discovery

### Initial Issue

Updating price with negative value returned: - HTTP 200 OK - Negative
price accepted

### Root Cause

Validation existed only in the constructor. Repository update directly
modified attributes without validation.

### Fix Implemented

Overrode update() method in Place model to enforce validation rules.

---

## 8. PUT Update Place -- Incorrect Status Code Bug

### Initial Issue

Validation error returned 404 instead of 400.

### Root Cause

PUT endpoint returned 404 for all ValueError exceptions.

### Fix Implemented

Updated PUT handler to: - Return 404 only for missing resource - Return
400 for validation errors

---

## 9. PUT Update Place -- Invalid Price (After Fix)

### cURL Command

    curl -i -X PUT "http://127.0.0.1:5000/api/v1/places/91ba90de-ab00-44b9-8159-2293aced8c6d" -H "Content-Type: application/json" -d '{
      "price": -50
    }'

Status: HTTP/1.1 400 BAD REQUEST

Response:

```json
{
  "error": "Price must be a positive value"
}
```

**Result:** PASS

---

## Summary

All Place endpoints were tested for: - Creation validation - Boundary
validation - Retrieval (all and specific) - Proper 404 handling - Update
validation - Correct HTTP status semantics

All identified defects were resolved and verified through retesting.
