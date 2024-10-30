from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_image():
    with open("test_image.jpg", "rb") as img:
        response = client.post(
            "/upload/",
            files={"file": ("test_image.jpg", img, "image/jpeg")},
            data={"title": "Test Image"}
        )
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_image():
    response = client.get("/images/1")
    assert response.status_code == 200
    assert "title" in response.json()
