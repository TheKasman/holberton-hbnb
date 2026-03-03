from app.models.review import Review 

def test_create_review_success(app):
    """Test successful review creation."""
    client = app.test_client()

    # First create a user and place if needed
    review = Review(
        user_id="Dave Davington",
        place_id="Google HQ",
        rating=5,
        text="Great!"
    )

    assert review.text == "Great place!"
    assert review.rating == 5
    assert review.user_id == "user1"
    assert review.place_id == "place1"


def test_review_has_id():
    """Review must inherit a UUID from BaseModel."""
    review = Review(
        text="Nice",
        rating=4,
        user_id="user1",
        place_id="place1"
    )

    assert review.id is not None


def test_review_empty_text():
    """Empty text must raise ValueError."""
    try:
        Review(
            text="",
            rating=5,
            user_id="user1",
            place_id="place1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_review_text_not_string():
    """Non-string text must raise ValueError."""
    try:
        Review(
            text=123,
            rating=5,
            user_id="user1",
            place_id="place1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_review_invalid_rating_low():
    """Rating below 1 must raise ValueError."""
    try:
        Review(
            text="Bad",
            rating=0,
            user_id="user1",
            place_id="place1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_review_invalid_rating_high():
    """Rating above 5 must raise ValueError."""
    try:
        Review(
            text="Too good",
            rating=6,
            user_id="user1",
            place_id="place1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_review_rating_not_integer():
    """Non-integer rating must raise ValueError."""
    try:
        Review(
            text="Wrong type",
            rating="five",
            user_id="user1",
            place_id="place1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_review_missing_user_id():
    """Missing user_id must raise ValueError."""
    try:
        Review(
            text="Nice",
            rating=4,
            user_id="",
            place_id="place1"
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_review_missing_place_id():
    """Missing place_id must raise ValueError."""
    try:
        Review(
            text="Nice",
            rating=4,
            user_id="user1",
            place_id=""
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    response = client.post("/api/v1/reviews/", json=review.to_dict())
    assert response.status_code == 400