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