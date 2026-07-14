# --- 1. 依存関係のインストールステージ ---
FROM node:20-slim AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

# --- 2. ビルドステージ ---
FROM node:20-slim AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 本番用にビルドを実行
RUN npm run build

# --- 3. 実行用ステージ（本番環境用） ---
FROM node:20-slim AS runner
WORKDIR /app

ENV NODE_ENV=production

# 実行に必要な最小限のファイルだけをビルド成果物からコピー
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# 本番サーバーのポート
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# standaloneモードでは、next start ではなく node server.js で起動します
CMD ["node", "server.js"]