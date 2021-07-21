from fastapi.testclient import TestClient

from main import app

test_app = TestClient(app)

valid_post = {
    "name": "valid",
    "username": "valid",
    "email": "valid@gmail.com",
    "phone": "+38012343253"
}

invalid_post = {
    "name": -228,
    "username": 101,
    "email": "notvalid",
    "phone": "+380"
}


def test_users():
    response = test_app.get("/users")
    assert response.status_code == 200


def test_create_user():
    response = test_app.post(
        "/users/",
        json=valid_post,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == "valid@gmail.com"
    assert data["username"] == "valid"
    assert data["name"] == "valid"
    assert data["phone"] == "+38012343253"
    assert "id" in data


def test_fail_create_user():
    response = test_app.post(
        "/users/",
        json=invalid_post,
    )
    assert response.status_code == 422

