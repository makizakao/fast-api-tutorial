import jwt
import pytest
from fastapi.testclient import TestClient

from backend.auth.util import SECRET_KEY, ALGORITHM
from backend.main import app

client = TestClient(app)


class TestUserLogin:
    """ユーザーログイン機能のテストクラス"""

    def test_login_success_with_valid_credentials(self):
        """正しいユーザー名とパスワードでログインが成功することを検証"""
        response = client.post(
            "/login",
            json={"username": "admin", "password": "password"}
        )

        # ステータスコード確認
        assert response.status_code == 200

        data = response.json()

        # レスポンス形式の検証
        assert "status" in data
        assert data["status"] == "success"
        assert "token" in data
        assert "user" in data

        # ユーザー情報の検証
        user = data["user"]
        assert user["username"] == "admin"
        assert "id" in user
        assert isinstance(user["id"], int)

        # トークンが有効なJWTか検証
        token = data["token"]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert "user_id" in decoded
        assert decoded["user_id"] == user["id"]

    def test_login_failure_with_non_existing_user(self):
        """存在しないユーザーでログインが失敗することを検証"""
        response = client.post(
            "/login",
            json={"username": "nonexistent_user", "password": "password"}
        )

        # ステータスコード確認（401 Unauthorized）
        assert response.status_code == 401

        data = response.json()
        assert "detail" in data
        assert "ユーザー名またはパスワードが正しくありません" in data["detail"]

    def test_login_failure_with_wrong_password(self):
        """パスワードが間違っている場合にログインが失敗することを検証"""
        response = client.post(
            "/login",
            json={"username": "admin", "password": "wrong_password"}
        )

        # ステータスコード確認（401 Unauthorized）
        assert response.status_code == 401

        data = response.json()
        assert "detail" in data
        assert "ユーザー名またはパスワードが正しくありません" in data["detail"]

    def test_login_request_schema_validation(self):
        """ログインリクエストのスキーマ検証"""
        # usernameが空の場合
        response = client.post(
            "/login",
            json={"username": "", "password": "password"}
        )
        # スキーマの検証に失敗する場合と、正常に進む場合がある
        # 実装にもよるが、ここでは空文字でクエリしても結果として失敗となることを確認
        assert response.status_code in [400, 401]

    def test_login_missing_required_fields(self):
        """必須フィールドが不足している場合の検証"""
        # usernameが欠落している場合
        response = client.post(
            "/login",
            json={"password": "password"}
        )
        assert response.status_code == 422  # Validation Error

        # passwordが欠落している場合
        response = client.post(
            "/login",
            json={"username": "admin"}
        )
        assert response.status_code == 422  # Validation Error

    def test_login_response_structure(self):
        """ログイン成功時のレスポンス構造の完全検証"""
        response = client.post(
            "/login",
            json={"username": "admin", "password": "password"}
        )

        assert response.status_code == 200
        data = response.json()

        # トップレベルのキーを検証
        required_keys = {"status", "token", "user"}
        assert required_keys.issubset(set(data.keys()))

        # userオブジェクトの検証
        user = data["user"]
        user_required_keys = {"id", "username"}
        assert user_required_keys.issubset(set(user.keys()))

        # userのデータ型を検証
        assert isinstance(user["id"], int)
        assert isinstance(user["username"], str)
        assert user["username"] == "admin"

        # トークンのデータ型を検証
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0

    def test_login_token_validity(self):
        """生成されたトークンが有効なJWTであることを検証"""
        response = client.post(
            "/login",
            json={"username": "admin", "password": "password"}
        )

        assert response.status_code == 200
        token = response.json()["token"]

        # トークンのデコードと検証
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            assert "user_id" in decoded
            assert "exp" in decoded
            assert isinstance(decoded["user_id"], int)
        except jwt.InvalidTokenError:
            pytest.fail("トークンのデコードに失敗しました")

    def test_login_case_sensitivity(self):
        """ユーザー名が大文字小文字を区別することを確認"""
        # "Admin"（大文字）でログインを試みる
        response = client.post(
            "/login",
            json={"username": "Admin", "password": "password"}
        )

        # adminは小文字なので失敗するはず
        assert response.status_code == 401

    def test_login_with_invalid_json(self):
        """不正なJSONでのログイン試行"""
        response = client.post(
            "/login",
            json={"username": "admin", "password": "password", "extra_field": "value"}
        )
        # 余分なフィールドがあっても無視される
        assert response.status_code == 200

    @pytest.mark.parametrize("username,password,expected_status", [
        ("admin", "password", 200),  # 正常系
        ("admin", "wrong", 401),  # パスワード間違い
        ("notfound", "password", 401),  # ユーザー未検出
        ("", "password", 401),  # 空のユーザー名
        ("admin", "", 401),  # 空のパスワード
    ])
    def test_login_parametrized(self, username, password, expected_status):
        """複数のテストケースをパラメータ化して検証"""
        response = client.post(
            "/login",
            json={"username": username, "password": password}
        )
        assert response.status_code == expected_status

        if expected_status == 200:
            data = response.json()
            assert data["user"]["username"] == username
