from app.models.review import Review #  Keeping this here just in case we need to instansiate a review

def test_create_review_success(app):
    client = app.test_client()

    # First create a user and place if needed

    review_data = {
        "user_id": "some-valid-user-id",
        "place_id": "some-valid-place-id",
        "rating": 5,
        "text": "Great!"
    }

    response = client.post("/api/v1/reviews/", json=review_data)
    assert response.status_code == 201