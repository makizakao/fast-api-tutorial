# Next.js + TypeScript

このフロントエンドは Next.js の App Router を使っています。`src/App.tsx` が記事一覧を表示するクライアントコンポーネントです。

## 使い方

```bash
cd frontend
npm install
npm run dev
```

ブラウザで `http://localhost:3000` を開くと、FastAPI の `/articles` を取得して表示します。

## 環境変数

`NEXT_PUBLIC_API_URL` にバックエンドの URL を設定します。

例:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## スクリプト

- `npm run dev` - 開発サーバー起動
- `npm run build` - 本番ビルド
- `npm run start` - 本番サーバー起動
- `npm run lint` - ESLint 実行
