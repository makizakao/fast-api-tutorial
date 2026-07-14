from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_get_articles_seeded_data():
    response = client.get("/articles")
    assert response.status_code == 200

    data = sorted(response.json(), key=lambda x: x["id"])

    # init.sql の投入件数を検証（例）
    assert len(data) == 3

    # 期待する完全一致（順序が保証される場合）
    expected = [
        {"id": 1, "title": "最初", "content": "これは最初の記事です。"},
        {"id": 2, "title": "二番目", "content": "これは二番目の記事です。"},
        {"id": 3, "title": "三番目", "content": "これは三番目の記事です。"},
    ]

    assert data == expected


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
