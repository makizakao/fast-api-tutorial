import {NextResponse} from 'next/server';
import {cookies} from 'next/headers';
import {getApiUrl} from "@/util/api-url";

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // FastAPIの /login エンドポイントへ中継
    const response = await fetch(getApiUrl(`/login`), {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
          {error: data.detail || 'ログインに失敗しました'},
          {status: response.status}
      );
    }

    // ログイン成功時、ブラウザのCookieにトークンを安全に保存
    const cookieStore = await cookies();
    cookieStore.set('auth_token', data.token, {
      httpOnly: true,     // JavaScriptから盗まれないようにするセキュリティ設定
      secure: process.env.NODE_ENV === 'production', // 本番(HTTPS)環境のみセキュアに
      sameSite: 'lax',
      maxAge: 60 * 60 * 24, // 有効期限: 1日間
      path: '/',          // アプリ全体で有効
    });

    // ログイン成功時のレスポンス
    return NextResponse.json(data);
  } catch (error) {
    console.error('Login routing error:', error);
    return NextResponse.json({error: 'Internal Server Error'}, {status: 500});
  }
}