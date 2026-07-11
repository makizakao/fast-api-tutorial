from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_articles():
    response = client.get("/articles")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert "id" in data[0]
    assert "title" in data[0]
    assert "content" in data[0]