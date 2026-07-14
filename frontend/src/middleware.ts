import type {NextRequest} from 'next/server';
import {NextResponse} from 'next/server';
import {getApiUrl} from "@/util/api-url";

export async function middleware(request: NextRequest) {
  // 1. クッキーから認証トークンを取得
  const token = request.cookies.get('auth_token')?.value;
  const {pathname} = request.nextUrl;

  if (
      pathname.startsWith('/_next') ||
      pathname.startsWith('/api/login') ||
      pathname.startsWith('/api/logout') ||
      pathname === '/login' ||
      pathname === '/favicon.ico'
  ) {
    return NextResponse.next();
  }

  if (!token) {
    if (pathname.startsWith('/api/')) {
      return NextResponse.json({error: 'Unauthorized'}, {status: 401});
    }
    return NextResponse.redirect(new URL('/login', request.url));
  }

  try {
    const backendRes = await fetch(getApiUrl('/verify-token'), {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}` // ブラウザから届いたトークンをFastAPIに投げる
      }
    });

    // 3. FastAPI側が「このトークンは偽造・無効だ！」と判断して401を返した場合
    if (backendRes.status === 401) {
      console.log('FastAPIがトークンの不正・改ざんを検知しました。一括ブロックします。');

      // APIへのアクセスなら401 JSONを自動返却
      if (pathname.startsWith('/api/')) {
        const response = NextResponse.json({error: 'Invalid Token'}, {status: 401});
        response.cookies.delete('auth_token');
        return response;
      }

      // 画面へのアクセスならクッキーを消去してログイン画面へ自動リダイレクト！
      const response = NextResponse.redirect(new URL('/login', request.url));
      response.cookies.delete('auth_token');
      return response;
    }
  } catch (error) {
    console.error('FastAPIへの接続エラー:', error);
  }

  // 問題なければそのまま画面を表示
  return NextResponse.next();
}

// ミドルウェアを適用するURLの範囲（対象外を定義する）
export const config = {
  matcher: [
    /*
     * 以下のパス【以外】のすべてのアクションにミドルウェアを適用する:
     * - _next/static (静的ファイル)
     * - _next/image (画像最適化)
     * - favicon.ico (ファビコン)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
};