from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.items.article import Article
from backend.models.articles import DBArticles

# 4. FastAPIアプリの初期化
app = FastAPI()

# CORSを許可する設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # ReactのURLを許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/articles", response_model=List[Article])
def get_articles(db: Session = Depends(get_db)):
    try:
        articles = db.query(DBArticles).all()
        return articles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
