from app.models.review import Review
import pytest

def test_create_review_success():
    """Test successful review creation."""
    review = Review(
        user_id="Dave Davington",
        place_id="Google HQ",
        rating=5,
        text="Great!"
    )
    assert review.text == "Great!"
    assert review.rating == 5
    assert review.user_id == "Dave Davington"
    assert review.place_id == "Google HQ"
    
    # from BaseModel // for some reason not working atm
    assert review.updated_at is not None
    assert review.created_at is not None
    assert review.id is not None

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
    with pytest.raises(ValueError):
        Review(
            text="",
            rating=5,
            user_id="user1",
            place_id="place1"
        )


def test_review_text_not_string():
    """Non-string text must raise ValueError."""
    with pytest.raises(ValueError):
        Review(
            text=123,
            rating=5,
            user_id="user1",
            place_id="place1"
        )


def test_review_invalid_rating_low():
    """Rating below 1 must raise ValueError."""
    with pytest.raises(ValueError):
        Review(
            text="Bad",
            rating=0,
            user_id="user1",
            place_id="place1"
        )


def test_review_invalid_rating_high():
    """Rating above 5 must raise ValueError."""
    with pytest.raises(ValueError):
        Review(
            text="Too good",
            rating=6,
            user_id="user1",
            place_id="place1"
        )


def test_review_rating_not_integer():
    """Non-integer rating must raise ValueError."""
    with pytest.raises(ValueError):
        Review(
            text="Wrong type",
            rating="five",
            user_id="user1",
            place_id="place1"
        )


def test_review_missing_user_id():
    """Missing user_id must raise ValueError."""
    with pytest.raises(ValueError):
        Review(
            text="Nice",
            rating=4,
            user_id="",
            place_id="place1"
        )


def test_review_missing_place_id():
    """Missing place_id must raise ValueError."""
    with pytest.raises(ValueError):
        Review(
            text="Nice",
            rating=4,
            user_id="user1",
            place_id=""
        )