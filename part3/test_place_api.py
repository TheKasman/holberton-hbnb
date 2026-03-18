from app import create_app
from app.services import facade


app = create_app()
app.config["TESTING"] = True
client = app.test_client()


def create_valid_user():
    response = client.post(
        "/api/v1/users/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john_test@example.com"
        }
    )
    return response.get_json()["id"]


def test_create_place_missing_title():
    user_id = create_valid_user()

    response = client.post(
        "/api/v1/places/",
        json={
            "price": 100,
            "latitude": 10,
            "longitude": 20,
            "owner_id": user_id
        }
    )

    assert response.status_code == 400


def test_create_place_negative_price():
    user_id = create_valid_user()

    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Invalid Price",
            "price": -10,
            "latitude": 10,
            "longitude": 20,
            "owner_id": user_id
        }
    )

    assert response.status_code == 400


def test_create_place_invalid_latitude():
    user_id = create_valid_user()

    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Bad Latitude",
            "price": 100,
            "latitude": 100,
            "longitude": 20,
            "owner_id": user_id
        }
    )

    assert response.status_code == 400


def test_create_place_invalid_longitude():
    user_id = create_valid_user()

    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Bad Longitude",
            "price": 100,
            "latitude": 10,
            "longitude": 200,
            "owner_id": user_id
        }
    )

    assert response.status_code == 400


def test_create_place_invalid_owner():
    response = client.post(
        "/api/v1/places/",
        json={
            "title": "Invalid Owner",
            "price": 100,
            "latitude": 10,
            "longitude": 20,
            "owner_id": "nonexistent-id"
        }
    )

    assert response.status_code == 400