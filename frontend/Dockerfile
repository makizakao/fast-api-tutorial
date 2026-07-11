FROM node:20-slim

WORKDIR /app

# パッケージ管理ファイルを先にコピーしてキャッシュを利かせる
COPY package*.json ./

# 依存ライブラリのインストール
RUN npm ci || npm install

# ソースコードをコピー
COPY . .

# Reactの開発サーバーが使用するポートを開放 (Viteは5173、CRAは3000が一般的ですが、3000番に統一して起動します)
EXPOSE 3000

ENTRYPOINT ["npx", "vite", "--host", "0.0.0.0", "--port", "3000"]