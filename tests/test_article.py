from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_articles_seeded_data():
    response = client.get("/articles")
    assert response.status_code == 200

    data = response.json()

    # init.sql の投入件数を検証（例）
    assert len(data) == 2

    # init.sql の1件目を検証（例）
    assert data[0]["id"] == 1
    assert data[0]["title"] == "最初"
    assert data[0]["content"] == "これは最初の記事です。"

    # init.sql の2件目を検証（例）
    assert data[1]["id"] == 2
    assert data[1]["title"] == "二番目"
    assert data[1]["content"] == "これは二番目の記事です。"

    # init.sql の3件目を検証（例）
    assert data[2]["id"] == 3
    assert data[2]["title"] == "三番目"
    assert data[2]["content"] == "これは三番目の記事です。"

def test_get_articles_schema():
    response = client.get("/articles")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for article in data:
        assert "id" in article
        assert "title" in article
        assert "content" in article