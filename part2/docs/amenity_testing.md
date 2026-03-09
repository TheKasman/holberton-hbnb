# Amenity Endpoint Testing Report

## Overview
This document logs the manual black-box testing performed on the Amenity
endpoints of the HBnB REST API. Tests were carried out using cURL against
a locally running Flask development server at http://127.0.0.1:5000.

---

## Environment

* Flask app running locally via Terminal
* Base URL: http://127.0.0.1:5000
* API Prefix: /api/v1
* Testing tool: cURL

---

## How to Reproduce Tests

1.  Start the Flask server:

```
    python3 run.py
```

2.  Run the cURL commands below exactly as written.

---

## Test 1 - Create an Amenity (POST /api/v1/amenities/)

**Command:**
`
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
`

**Input:**
```json
{ "name": "Wi-Fi" }
```

**Expected:** 201 Created - returns amenity object with a generated ID

**Actual:**
```json
{
	"id": "a0ed107c-be43-4375-a4ae-0c07cb1f5ab6",
  "name": "Wi-Fi",
  "created_at": "2026-03-09T03:19:27.428888",
  "updated_at": "2026-03-09T03:19:27.428893"
}
```

**Status Code:** 201
**Result:** PASS

---

## Test 2 - Retrieve All Amenities (GET /api/v1/amenities/)

**Command:**
`
curl http://127.0.0.1:5000/api/v1/amenities/
`

**Input:** None

**Expected:** 200 OK - returns a list containing the previously created amenity

**Actual:**
```json
[
    {
        "id": "a0ed107c-be43-4375-a4ae-0c07cb1f5ab6",
        "name": "Wi-Fi",
        "created_at": "2026-03-09T03:19:27.428888",
        "updated_at": "2026-03-09T03:19:27.428893"
    }
]
```

**Status Code:** 200
**Result:** PASS

---

## Test 3 - Retrieve a Single Amenity by ID (GET /api/v1/amenities/<id>)

**Command:**
`
curl http://127.0.0.1:5000/api/v1/amenities/a0ed107c-be43-4375-a4ae-0c07cb1f5ab6
`

**Input:** Valid amenity ID from Test 1

**Expected:** 200 OK - returns the amenity object matching the given ID

**Actual:**
```json
{
  "id": "a0ed107c-be43-4375-a4ae-0c07cb1f5ab6",
  "name": "Wi-Fi",
  "created_at": "2026-03-09T03:19:27.428888",
  "updated_at": "2026-03-09T03:19:27.428893"
}
```

**Status Code:** HTTP 1.1/ 200 OK

**Result:** PASS

---

## Test 4 - Update an Amenity (PUT /api/v1/amenities/<id>)

**Command:**
`
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/a0ed107c-be43-4375-a4ae-0c07cb1f5ab6 \
  -H "Content-Type: application/json" \
  -d '{"name": "Free Wi-Fi"}'
`

**Input:**
```json
{ "name": "Free Wi-Fi" }
```

**Expected:** 200 OK - returns success message confirming update

**Actual:**
```json
{
  "id": "a0ed107c-be43-4375-a4ae-0c07cb1f5ab6",
  "name": "Free Wi-Fi",
  "created_at": "2026-03-09T03:19:27.428888",
  "updated_at": "2026-03-09T03:19:27.428893"
}
```

**Status Code:** HTTP 1.1/ 200 OK

**Result:** PASS

---

## Test 5 - Create Amenity with Invalid Input (POST /api/v1/amenities/)

**Command:**
`
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
`

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

**Status Code:** HTTP/1.1 400 BAD REQUEST

**Result:** PASS

---

## Test 6 - Update Amenity with Invalid Input (PUT /api/v1/amenities/<id>)

**Command:**
`
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \a0ed107c-be43-4375-a4ae-0c07cb1f5ab6 \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'
`

**Input:**
```json
{ "name": "" }
```

**Expected:** 400 Bad Request - empty name should be rejected by validation

**Actual:**
```json
{
  "error": "Amenity name must be a non-empty string of max 50 characters"
}
```

**Status Code:** HTTP/1.1 400 BAD REQUEST

**Result:** PASS

---

**All 6 tests passed.**