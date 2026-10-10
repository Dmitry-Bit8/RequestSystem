import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.post("/users/register", json={
        "email": "new@example.com",
        "full_name": "New User",
        "password": "password123",
        "role": "requester"
    })
    assert response.status_code == 201
    assert "email" in response.json()
    assert "password" not in response.json()


def test_register_duplicate_user(client: TestClient):
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "full_name": "Test",
        "password": "testpassword123",
        "role": "admin"
    })
    assert response.status_code == 400


def test_login_success(client: TestClient):
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client: TestClient):
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_wrong_email(client: TestClient):
    response = client.post("/users/login", json={
        "email": "nonexistent@example.com",
        "password": "testpassword123"
    })
    assert response.status_code == 401


def test_get_me(client: TestClient):
    login = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_list_users_as_admin(client: TestClient):
    login = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_request(client: TestClient):
    login = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/requests/", headers=headers, json={
        "title": "Test Request",
        "description": "This is a test request description",
        "priority": "high",
        "category_id": 1
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Request"


def test_get_requests(client: TestClient):
    login = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/requests/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_statuses(client: TestClient):
    login = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/statuses/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_categories(client: TestClient):
    login = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/categories/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_health_check(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
