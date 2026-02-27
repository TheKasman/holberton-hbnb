import pytest
from app import create_app
from app.services import facade


@pytest.fixture(autouse=True)
def reset_repositories():
    facade.user_repo.clear()
    facade.place_repo.clear()
    facade.review_repo.clear()
    facade.amenity_repo.clear()


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()