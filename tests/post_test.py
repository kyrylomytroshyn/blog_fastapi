from fastapi.testclient import TestClient

from main import app

test_app = TestClient(app)

valid_post = {
    "userId": 1,
    "title": "TITLE",
    "body": "THIS BODY"
}

invalid_post = {
    "userId": "1",
    "tit": 123,
    "bodsy": 123
}


def test_posts():
    response = test_app.get("/posts")
    assert response.status_code == 200
    resp = response.json()[0]
    assert resp["author"]["id"]
    assert resp["author"]["name"]
    assert resp["author"]["phone"]
    assert resp["author"]["email"]
    assert resp["author"]["username"]


def test_posts_details():
    response = test_app.get("/posts/1")
    assert response.status_code == 200
    resp = response.json()
    assert "id" in resp
    assert "title" in resp
    assert "body" in resp
    assert "author" in resp
    assert resp["comments"]


def test_post_update():
    response = test_app.get("/posts/1", json=valid_post)
    assert response.status_code == 200
    resp = response.json()
    assert "id" in resp
    assert "title" in resp
    assert "body" in resp
    assert "author" in resp
    assert resp["comments"]


def test_post_create():
    response = test_app.post("/posts/", json=valid_post)
    assert response.status_code == 201
    resp = response.json()
    assert "id" in resp
    assert "title" in resp
    assert "body" in resp
    assert "author" in resp
    assert resp['title'] == "TITLE"
    assert resp['body'] == "THIS BODY"


def test_post_update_fail():
    response = test_app.post("/posts/1", json=invalid_post)
    assert response.status_code == 405
    response = test_app.put("/posts/1", json=invalid_post)
    assert response.status_code == 422


def test_post_create_fail():
    response = test_app.post("/posts/", json=invalid_post)
    assert response.status_code == 422
