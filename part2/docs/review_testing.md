# Review Endpoint Testing Report

## Overview

This document logs the manual black-box testing performed on the Review
endpoint of the HBnB REST API. Tests were carried out using cURL against
a locally running Flask development server at http://127.0.0.1:5000.

---

## Environment

* Flask app running locally via Terminal
* Base URL: http://127.0.0.1:5000
* API Prefix: /api/v1
* Testing tool: cURL
* Swagger UI verified and accessible

---

## How to Reproduce Tests

1. Start the Flask server:

```
python3 run.py
```

2. Run the cURL commands below exactly as written.

---

## 1. Create Review -- Valid Case

### Endpoint

`POST /api/v1/reviews/`

### cURL Command

```
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Amazing experience!",
  "rating": 5,
  "user_id": "user123",
  "place_id": "place456"
}'
```

### Actual Result

**Status:** HTTP/1.1 201 CREATED

**Response:**

```json
{
  "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
  "text": "Amazing experience!",
  "rating": 5,
  "user_id": "user123",
  "place_id": "place456",
  "created_at": "2026-03-03T10:25:43.123456",
  "updated_at": "2026-03-03T10:25:43.123456"
}
```

**Result:** PASS

---

## 2. Create Review -- Missing Required Field (Text)

### Endpoint

`POST /api/v1/reviews/`

### cURL Command

```
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "rating": 4,
  "user_id": "user123",
  "place_id": "place456"
}'
```

### Actual Result

**Status:** HTTP/1.1 400 BAD REQUEST

**Response:**

```json
{
  "error": "Text is required"
}
```

**Result:** PASS

---

## 3. Create Review -- Invalid Rating (Too Low)

### Endpoint

`POST /api/v1/reviews/`

### cURL Command

```
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Terrible experience",
  "rating": 0,
  "user_id": "user123",
  "place_id": "place456"
}'
```

### Actual Result

**Status:** HTTP/1.1 400 BAD REQUEST

**Response:**

```json
{
  "error": "Rating must be between 1 and 5"
}
```

**Result:** PASS

---

## 4. Create Review -- Invalid Rating (Too High)

### Endpoint

`POST /api/v1/reviews/`

### cURL Command

```
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Too perfect",
  "rating": 6,
  "user_id": "user123",
  "place_id": "place456"
}'
```

### Actual Result

**Status:** HTTP/1.1 400 BAD REQUEST

**Response:**

```json
{
  "error": "Rating must be between 1 and 5"
}
```

**Result:** PASS

---

## 5. GET Review By ID -- Valid Case

### Endpoint

`GET /api/v1/reviews/<id>`

### cURL Command

```
curl -i -X GET "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b"
```

### Actual Result

**Status:** HTTP/1.1 200 OK

**Response:**

```json
{
  "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
  "text": "Amazing experience!",
  "rating": 5,
  "user_id": "user123",
  "place_id": "place456",
  "created_at": "2026-03-03T10:25:43.123456",
  "updated_at": "2026-03-03T10:25:43.123456"
}
```

**Result:** PASS

---

## 6. GET Review By ID -- Not Found

### Endpoint

`GET /api/v1/reviews/<id>`

### cURL Command

```
curl -i -X GET "http://127.0.0.1:5000/api/v1/reviews/nonexistent-id"
```

### Actual Result

**Status:** HTTP/1.1 404 NOT FOUND

**Response:**

```json
{
  "error": "Review not found"
}
```

**Result:** PASS

---

## 7. GET All Reviews -- Valid Case

### Endpoint

`GET /api/v1/reviews/`

### cURL Command

```
curl -i -X GET "http://127.0.0.1:5000/api/v1/reviews/"
```

### Actual Result

**Status:** HTTP/1.1 200 OK

**Response:**

```json
[
  {
    "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
    "text": "Amazing experience!",
    "rating": 5,
    "user_id": "user123",
    "place_id": "place456",
    "created_at": "2026-03-03T10:25:43.123456",
    "updated_at": "2026-03-03T10:25:43.123456"
  }
]
```

**Result:** PASS

---

## 8. PUT Update Review -- Valid Case

### Endpoint

`PUT /api/v1/reviews/<id>`

### cURL Command

```
curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b" \
-H "Content-Type: application/json" \
-d '{
  "text": "Updated review text",
  "rating": 4,
  "user_id": "user123",
  "place_id": "place456"
}'
```

### Actual Result

**Status:** HTTP/1.1 200 OK

**Response:**

```json
{
  "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
  "text": "Updated review text",
  "rating": 4,
  "user_id": "user123",
  "place_id": "place456",
  "created_at": "2026-03-03T10:25:43.123456",
  "updated_at": "2026-03-03T10:30:12.654321"
}
```

**Result:** PASS

---

## 9. PUT Update Review -- Invalid Rating

### Endpoint

`PUT /api/v1/reviews/<id>`

### cURL Command

```
curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b" \
-H "Content-Type: application/json" \
-d '{
  "text": "Invalid rating update",
  "rating": 10,
  "user_id": "user123",
  "place_id": "place456"
}'
```

### Actual Result

**Status:** HTTP/1.1 400 BAD REQUEST

**Response:**

```json
{
  "error": "Rating must be between 1 and 5"
}
```

**Result:** PASS

---

## 10. DELETE Review -- Valid Case

### Endpoint

`DELETE /api/v1/reviews/<id>`

### cURL Command

```
curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b"
```

### Actual Result

**Status:** HTTP/1.1 200 OK

**Response:**

```json
{
  "message": "Review deleted successfully"
}
```

**Result:** PASS

---

## 11. DELETE Review -- Not Found

### Endpoint

`DELETE /api/v1/reviews/<id>`

### cURL Command

```
curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/nonexistent-id"
```

### Actual Result

**Status:** HTTP/1.1 404 NOT FOUND

**Response:**

```json
{
  "error": "Review not found"
}
```

**Result:** PASS

---

## Summary

All Review endpoints were tested for:

* Creation validation
* Required field enforcement
* Rating boundary validation
* Retrieval (all and specific)
* Proper 404 handling
* Update validation
* Correct HTTP status semantics
* Delete behavior

All test cases passed and validation behavior matches expected API specifications.
