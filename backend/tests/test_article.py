from datetime import datetime, timezone, timedelta

import jwt
from fastapi.testclient import TestClient

from backend.auth.util import SECRET_KEY, ALGORITHM
from backend.main import app

client = TestClient(app)


def get_test_auth_headers():
    """テスト用に有効期限24時間の有効なJWTトークンヘッダーを生成するヘルパー関数"""
    expire = datetime.now(timezone.utc) + timedelta(days=1)

    # プログラム側の仕様に合わせてペイロードを組み立てます
    # もしプログラム側を「user_id」にした場合は以下を {"user_id": 1, ...} にしてください
    token_data = {
        "sub": "1",  # テストユーザーID (admin)
        "username": "admin",  # テストユーザー名
        "exp": expire
    }

    # 秘密鍵で暗号署名
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"Authorization": f"Bearer {token}"}


def test_get_articles_seeded_data():
    headers = get_test_auth_headers()
    response = client.get("/articles", headers=headers)

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
    headers = get_test_auth_headers()
    response = client.get("/articles", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for article in data:
        assert "id" in article
        assert "title" in article
        assert "content" in article
