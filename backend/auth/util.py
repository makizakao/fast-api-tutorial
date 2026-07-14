# Next.jsからヘッダー経由でトークンを受け取るための設定
from datetime import timedelta, datetime, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


def get_current_user(token: str = Depends(api_key_header)):
    """トークンの署名と有効期限を検証し、偽造されていれば401エラーを出す関数"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンが見つかりません"
        )

    try:
        # Bearer プレフィックスが付いている場合は除去
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        # 秘密鍵を使ってトークンを複合・検証。改ざんされていればここでエラーになる
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # 検証成功ならトークンの中身（user_idなど）を返す

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="トークンの有効期限が切れています")
    except jwt.InvalidTokenError:
        # ユーザーがクッキーを書き換えた（偽造した）場合は必ずここに入ります！
        raise HTTPException(status_code=401, detail="不正な認証トークンです")


def create_access_token(user):
    """ユーザー情報をもとにJWTトークンを生成する関数"""
    expire = datetime.now(timezone.utc) + timedelta(days=1)
    token = jwt.encode({"user_id": user.id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return token
