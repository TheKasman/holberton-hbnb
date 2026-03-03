
### Review Testing

### 1. Create Review — Valid Case
Endpoint

`POST /api/v1/reviews/`

cURL Command
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Amazing experience!",
  "rating": 5,
  "user_id": "user123",
  "place_id": "place456"
}'
Actual Result

Status: HTTP/1.1 201 CREATED

Response:
{
    "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
    "text": "Amazing experience!",
    "rating": 5,
    "user_id": "user123",
    "place_id": "place456",
    "created_at": "2026-03-03T10:25:43.123456",
    "updated_at": "2026-03-03T10:25:43.123456"
}
2. Create Review — Missing Required Field (Text)
Endpoint

POST /api/v1/reviews/

Steps

Attempt to create a review without the text field

cURL Command
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "rating": 4,
  "user_id": "user123",
  "place_id": "place456"
}'
Actual Result

Status: HTTP/1.1 400 BAD REQUEST

Response:
{
    "error": "Text is required"
}
3. Create Review — Invalid Rating (Too Low)
Endpoint

POST /api/v1/reviews/

cURL Command
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Terrible experience",
  "rating": 0,
  "user_id": "user123",
  "place_id": "place456"
}'
Actual Result

Status: HTTP/1.1 400 BAD REQUEST

Response:
{
    "error": "Rating must be between 1 and 5"
}
4. Create Review — Invalid Rating (Too High)
Endpoint

POST /api/v1/reviews/

cURL Command
curl -i -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-d '{
  "text": "Too perfect",
  "rating": 6,
  "user_id": "user123",
  "place_id": "place456"
}'
Actual Result

Status: HTTP/1.1 400 BAD REQUEST

Response:
{
    "error": "Rating must be between 1 and 5"
}
5. Get Review By ID — Valid Case
Endpoint

GET /api/v1/reviews/<id>

cURL Command
curl -i -X GET "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b"
Actual Result

Status: HTTP/1.1 200 OK

Response:
{
    "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
    "text": "Amazing experience!",
    "rating": 5,
    "user_id": "user123",
    "place_id": "place456",
    "created_at": "2026-03-03T10:25:43.123456",
    "updated_at": "2026-03-03T10:25:43.123456"
}
6. Get Review By ID — Not Found
Endpoint

GET /api/v1/reviews/<id>

cURL Command
curl -i -X GET "http://127.0.0.1:5000/api/v1/reviews/nonexistent-id"
Actual Result

Status: HTTP/1.1 404 NOT FOUND

Response:
{
    "error": "Review not found"
}
7. List All Reviews — Valid Case
Endpoint

GET /api/v1/reviews/

cURL Command
curl -i -X GET "http://127.0.0.1:5000/api/v1/reviews/"
Actual Result

Status: HTTP/1.1 200 OK

Response:
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
8. Update Review — Valid Case
Endpoint

PUT /api/v1/reviews/<id>

cURL Command
curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b" \
-H "Content-Type: application/json" \
-d '{
  "text": "Updated review text",
  "rating": 4,
  "user_id": "user123",
  "place_id": "place456"
}'
Actual Result

Status: HTTP/1.1 200 OK

Response:
{
    "id": "9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b",
    "text": "Updated review text",
    "rating": 4,
    "user_id": "user123",
    "place_id": "place456",
    "created_at": "2026-03-03T10:25:43.123456",
    "updated_at": "2026-03-03T10:30:12.654321"
}
9. Update Review — Invalid Rating
Endpoint

PUT /api/v1/reviews/<id>

cURL Command
curl -i -X PUT "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b" \
-H "Content-Type: application/json" \
-d '{
  "text": "Invalid rating update",
  "rating": 10,
  "user_id": "user123",
  "place_id": "place456"
}'
Actual Result

Status: HTTP/1.1 400 BAD REQUEST

Response:
{
    "error": "Rating must be between 1 and 5"
}
10. Delete Review — Valid Case
Endpoint

DELETE /api/v1/reviews/<id>

cURL Command
curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/9f4c6c88-9b61-4c73-a4b2-3f8eaf1e6a1b"
Actual Result

Status: HTTP/1.1 200 OK

Response:
{
    "message": "Review deleted successfully"
}
11. Delete Review — Not Found
Endpoint

DELETE /api/v1/reviews/<id>

cURL Command
curl -i -X DELETE "http://127.0.0.1:5000/api/v1/reviews/nonexistent-id"
Actual Result

Status: HTTP/1.1 404 NOT FOUND

Response:
{
    "error": "Review not found"
}