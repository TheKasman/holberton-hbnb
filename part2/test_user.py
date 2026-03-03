#!/usr/bin/python3
from app.models.user import User

#  ===========================================
#  |   USER CREATION - BUSINESS LOGIC TEST   |
#  ===========================================

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value

#  ===============
#  |  API TESTS  |
#  ===============
#  ===============================
#  |   USER CREATION - API TEST  |
#  ===============================

def test_create_user(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })

    assert response.status_code == 201

    data = response.get_json()
    assert "id" in data
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john.doe@example.com"

#  ======================================
#  |   USER CREATION - DUPLICATE EMAIL  |
#  ======================================

def test_create_user_duplicate_email(client):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    client.post("/api/v1/users/", json=payload)
    response = client.post("/api/v1/users/", json=payload)

    assert response.status_code == 400

#  =============================
#  |   USER CREATION - GET ID  |
#  =============================

def test_get_user_by_id(client):
    response = client.post("/api/v1/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    print(response.get_json())
    
    user_id = response.get_json()["id"]

    get_response = client.get(f"/api/v1/users/{user_id}")

    assert get_response.status_code == 200
    assert get_response.get_json()["id"] == user_id

#  =========================================
#  |   USER CREATION - 404 USER NOT FOUND  |
#  =========================================

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/nonexistent-id")
    assert response.status_code == 404

#  ================================================================
#  |   USER CREATION - POPULATE ONE USER, LIST THE CURRENT USERS  |
#  ================================================================

def test_list_users(client):
    client.post("/api/v1/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })

    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

#  ====================================
#  |   USER CREATION - UPDATE A USER  |
#  ====================================

def test_update_user(client):
    create = client.post("/api/v1/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })

    user_id = create.get_json()["id"]

    update_response = client.put(f"/api/v1/users/{user_id}", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com"
    })

    assert update_response.status_code == 200
    assert update_response.get_json()["first_name"] == "Jane"
