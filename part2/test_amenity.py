from app.models.amenity import Amenity

def test_amenity_creation():
    """Basic creation stores the name correctly."""
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"

def test_amenity_has_id():
    """Amenity must inherit a UUID from BaseModel."""
    amenity = Amenity(name="Pool")
    assert amenity.id is not None

def test_amenity_empty_name():
    """An empty name must raise a ValueError."""
    try:
        Amenity(name="")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_amenity_name_too_long():
    """A name over 50 characters must raise a ValueError."""
    try:
        Amenity(name="A" * 51)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_amenity_name_not_string():
    """A non-string name must raise a ValueError."""
    try:
        Amenity(name=123)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
