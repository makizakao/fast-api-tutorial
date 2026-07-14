/**
 * 共通のバックエンドURLを取得し、指定されたパスと結合するヘルパー関数
 * @param path 結合したいパス (例: '/articles', '/verify-token')
 */
export function getApiUrl(path: string): string {
  // 環境変数を取得（未設定時のローカルフォールバックもここに集約）
  const baseUrl = process.env.BACKEND_API_URL ?? 'http://backend:8000';

  // スラッシュの重複を防いで綺麗にURLを結合
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${baseUrl}${cleanPath}`;
}