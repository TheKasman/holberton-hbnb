
## 1. Create User -- Valid Case

### Endpoint
`POST /api/v1/users/`

### cURL Command
`curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \  -H "Content-Type: application/json" \  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com" }'`

### Actual Result
Status: HTTP/1.1 201 CREATED
```
Response:
{
    "id": "322b1710-0c3d-409a-9e68-22e5fe5013ec",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

## 2. Create User -- Duplicate Email

### Endpoint
`POST /api/v1/users/`

### Steps
1. Create user with email john.doe@example.com
2. Attempt to create the same user again

### cURL Command
`curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}'`

### Actual Result
Status: HTTP/1.1 400 BAD REQUEST
```
Response:
{
    "error": "Email already registered"
}
```

## 3. Get User By ID -- Valid Case

### Endpoint
`GET /api/v1/users/`

### cURL Command
`curl -i -X GET "http://127.0.0.1:5000/api/v1/users/<id>"`

### Actual Result
Status: HTTP/1.1 200 OK
```
Response:
{
    "id": "322b1710-0c3d-409a-9e68-22e5fe5013ec",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

## 4. Get User By ID -- User Not Found

### Endpoint
`GET /api/v1/users/<id>`
### cURL Command
`curl -i -X GET "http://127.0.0.1:5000/api/v1/users/<id>"`

### Actual Result
Status: HTTP/1.1 404 NOT FOUND
```
Response:
{
    "error": "User not found"
}
```

## 5. List All Users -- Valid Case

### Endpoint
GET /api/v1/users/

### cURL Command
`curl -i -X GET "http://127.0.0.1:5000/api/v1/users/"`

### Actual Result
Status: HTTP/1.1 200 OK
```
Response:
[
    {
        "id": "322b1710-0c3d-409a-9e68-22e5fe5013ec",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
]
```

## 6. Update User -- Valid case
### Endpoint
`PUT /api/v1/users/<id>`

### cURL Command
`curl -i -X PUT "http://127.0.0.1:5000/api/v1/users/<id>" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}'`

### Actual Response
Status: HTTP/1.1 200 OK
```
Response: 
{
    "id": "322b1710-0c3d-409a-9e68-22e5fe5013ec",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
}
```