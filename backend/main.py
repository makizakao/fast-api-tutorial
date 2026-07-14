from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.auth.util import get_current_user, create_access_token
from backend.database import get_db
from backend.models.articles import Articles
from backend.models.users import Users
from backend.schemas.article_response import ArticleResponse
from backend.schemas.login_request import LoginRequest

# 4. FastAPIアプリの初期化
app = FastAPI()

# CORSを許可する設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ReactのURLを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/articles", response_model=List[ArticleResponse])
def get_articles(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    try:
        articles = db.query(Articles).all()
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/verify-token")
def verify_token(_: dict = Depends(get_current_user)):
    return {"status": "success", "message": "Token is valid"}


@app.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """ハッシュ化をせず、平文でパスワードを直接比較するログインエンドポイント"""
    try:
        # 1. データベースからユーザー名が一致するレコードを取得
        user = db.query(Users).filter(Users.username == payload.username).first()

        # ユーザーが存在しない、またはパスワードが完全に一致しない場合
        if not user or user.password != payload.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="ユーザー名またはパスワードが正しくありません"
            )
        token = create_access_token(user)  # JWTトークンを生成

        # 2. 認証成功時のレスポンス
        return {
            "status": "success",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username
            }
        }

    except HTTPException:
        # 認証失敗のHTTPExceptionはそのままフロントエンドに返す
        raise
    except Exception as e:
        # それ以外のDBエラーなどは500で返す
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during login: {str(e)}"
        )
