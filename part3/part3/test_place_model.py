from app.models.place import Place
from app.models.user import User
import pytest


# ==========================================================
# VALID CREATION
# ==========================================================

def test_place_valid_creation():
    owner = User("John", "Doe", "john@example.com")

    place = Place(
        title="Beach House",
        description="Nice place",
        price=100.0,
        latitude=10.0,
        longitude=20.0,
        owner=owner
    )

    assert place.title == "Beach House"
    assert place.price == 100.0


# ==========================================================
# TITLE VALIDATION
# ==========================================================

def test_place_invalid_title_empty():
    owner = User("John", "Doe", "john@example.com")

    with pytest.raises(ValueError):
        Place(
            title="",
            price=100.0,
            latitude=10.0,
            longitude=20.0,
            owner=owner
        )


# ==========================================================
# PRICE VALIDATION
# ==========================================================

def test_place_invalid_price_zero():
    owner = User("John", "Doe", "john@example.com")

    with pytest.raises(ValueError):
        Place(
            title="Test",
            price=0,
            latitude=10.0,
            longitude=20.0,
            owner=owner
        )


def test_place_invalid_price_negative():
    owner = User("John", "Doe", "john@example.com")

    with pytest.raises(ValueError):
        Place(
            title="Test",
            price=-10,
            latitude=10.0,
            longitude=20.0,
            owner=owner
        )


# ==========================================================
# LATITUDE VALIDATION
# ==========================================================

def test_place_invalid_latitude():
    owner = User("John", "Doe", "john@example.com")

    with pytest.raises(ValueError):
        Place(
            title="Test",
            price=100,
            latitude=100.0,
            longitude=20.0,
            owner=owner
        )


# ==========================================================
# LONGITUDE VALIDATION
# ==========================================================

def test_place_invalid_longitude():
    owner = User("John", "Doe", "john@example.com")

    with pytest.raises(ValueError):
        Place(
            title="Test",
            price=100,
            latitude=10.0,
            longitude=200.0,
            owner=owner
        )