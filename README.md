# Fast API Tutorial

FastAPI と React を使ったシンプルな Web アプリケーション。PostgreSQL データベースに記事データを保存し、API 経由で取得・表示します。

## プロジェクト構成

```
fast-api-tutorial/
├── backend/              # FastAPI バックエンド
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py          # FastAPI アプリ
│   ├── database.py       # DB 接続設定
│   ├── items/
│   │   └── article.py   # Pydantic スキーマ
│   ├── models/
│   │   └── articles.py  # SQLAlchemy モデル
│   └── tests/
│       └── test_article.py
├── frontend/             # React フロントエンド
│   ├── src/
│   │   └── App.jsx
│   └── ...
├── docker-compose.yml
└── init.sql             # DB 初期化スクリプト
```

## 必要な環境

- Docker
- Docker Compose

## セットアップ

### 1. Docker イメージをビルド・起動

```bash
docker compose up -d
```

### 2. バックエンド確認

API サーバーが起動しています:
- **API**: http://localhost:8000/articles
- **ドキュメント**: http://localhost:8000/docs

### 3. フロントエンド起動（別ターミナル）

```bash
cd frontend
npm install
npm start
```

フロントエンドが起動します: http://localhost:3000

## テスト実行

バックエンドのテストを実行:

```bash
docker compose exec backend env PYTHONPATH=. pytest
```

## DB 初期化

`init.sql` によって以下の記事データが自動で投入されます:

- ID 1: 「最初」
- ID 2: 「二番目」
- ID 3: 「三番目」

## API エンドポイント

### 記事一覧取得

```
GET /articles
```

**レスポンス例:**

```json
[
  {
    "id": 1,
    "title": "最初",
    "content": "これは最初の記事です。"
  },
  {
    "id": 2,
    "title": "二番目",
    "content": "これは二番目の記事です。"
  },
  {
    "id": 3,
    "title": "三番目",
    "content": "これは三番目の記事です。"
  }
]
```

## 停止

```bash
docker compose down
```

## ファイル説明

- `backend/main.py`: FastAPI アプリのメインファイル
- `backend/database.py`: SQLAlchemy の DB 接続設定
- `backend/models/articles.py`: DB テーブル定義
- `backend/items/article.py`: API レスポンス用 Pydantic スキーマ
- `frontend/src/App.jsx`: React コンポーネント
- `docker-compose.yml`: Docker Compose の設定
- `init.sql`: PostgreSQL の初期化スクリプト
