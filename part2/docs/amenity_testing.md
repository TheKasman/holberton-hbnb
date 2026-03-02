# Amenity Endpoint Testing Report

## Overview
This document logs the manual black-box testing performed on the Amenity
endpoints of the HBnB REST API. Tests were carried out using cURL against
a locally running Flask development server at http://127.0.0.1:5000.

---

## Test 1 - Create an Amenity (POST /api/v1/amenities/)

**Command:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

**Input:**
```json
{ "name": "Wi-Fi" }
```

**Expected:** 201 Created - returns amenity object with a generated ID

**Actual:**
```json
{
	"id": "539e211c-9eab-4df9-ad2d-7b59d6ce3475",
	"name": "Wi-Fi"
}
```

**Status Code:** 201
**Result:** PASS

---

## Test 2 - Retrieve All Amenities (GET /api/v1/amenities/)

**Command:**
```bash
curl http://127.0.0.1:5000/api/v1/amenities/
```

**Input:** None

**Expected:** 200 OK - returns a list containing the previously created amenity

**Actual:**
```json
[
    {
        "id": "539e211c-9eab-4df9-ad2d-7b59d6ce3475",
        "name": "Wi-Fi"
    }
]
```

**Status Code:** 200
**Result:** PASS

---

## Test 3 - Retrieve a Single Amenity by ID (GET /api/v1/amenities/<id>)

**Command:**
```bash
curl http://127.0.0.1:5000/api/v1/amenities/539e211c-9eab-4df9-ad2d-7b59d6ce3475
```

**Input:** Valid amenity ID from Test 1

**Expected:** 200 OK - returns the amenity object matching the given ID

**Actual:**
```json
{
    "id": "539e211c-9eab-4df9-ad2d-7b59d6ce3475",
    "name": "Wi-Fi"
}
```

**Status Code:** 200
**Result:** PASS

> **Note:** The original test used a different ID
> (fadb59b0-2a97-4f8e-92aa-9507bb8c5c45) from a previous session.
> Since the app uses in-memory storage, data does not persist between
> restarts. The correct ID from this session is
> 539e211c-9eab-4df9-ad2d-7b59d6ce3475.

---

## Test 4 - Update an Amenity (PUT /api/v1/amenities/<id>)

**Command:**
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/539e211c-9eab-4df9-ad2d-7b59d6ce3475 \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Wi-Fi"}'
```

**Input:**
```json
{ "name": "Free Wi-Fi" }
```

**Expected:** 200 OK - returns success message confirming update

**Actual:**
```json
{
    "message": "Amenity updated successfully"
}
```

**Status Code:** 200
**Result:** PASS

> **Note:** An earlier attempt failed with a space in the URL
> (amenities/ <id>) and an AttributeError caused by a double-call bug
> in the facade - update() was being called both manually and via the
> repository. Both issues were resolved before this test passed.

---

## Test 5 - Create Amenity with Invalid Input (POST /api/v1/amenities/)

**Command:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
```

**Input:**
```json
{ "name": "" }
```

**Expected:** 400 Bad Request - empty name should be rejected by model validation

**Actual:**
```json
{
    "error": "Amenity name must be a non-empty string of max 50 characters"
}
```

**Status Code:** 400
**Result:** PASS

---

**All 5 tests passed.**