from fastapi.testclient import TestClient
from main import app, users, User
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_user_success():
    response = client.get("/users/0")
    assert response.status_code == 200
    assert response.json()["name"] == "An"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Không tìm thấy user"


def test_create_user_success():
    new_user = {"name": "Dung", "age": 28, "city": "Da Nang"}
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    assert response.json()["name"] == "Dung"


def test_create_user_invalid_age():
    # Thử gửi age là chuỗi chữ thay vì số -> Pydantic bắt lỗi 422
    invalid_user = {"name": "Em", "age": "abc", "city": "Hue"}
    response = client.post("/users", json=invalid_user)
    assert response.status_code == 422


def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "average_age" in data
    assert "cities" in data
    assert data["count"] == len(users)


def test_delete_user_success():
    initial_count = len(users)
    response = client.delete("/users/0")
    assert response.status_code == 200
    assert response.json()["name"] == "An"
    assert len(users) == initial_count - 1


def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Không tìm thấy user"
