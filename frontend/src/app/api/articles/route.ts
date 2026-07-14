import {NextResponse} from 'next/server';
import {cookies} from 'next/headers';
import {getApiUrl} from "@/util/api-url";


export async function GET() {
  try {
    // ブラウザのクッキーから auth_token を取得
    const cookieStore = await cookies();
    const token = cookieStore.get('auth_token')?.value;

    // Next.jsサーバーからFastAPI（backend）へリクエスト
    const response = await fetch(getApiUrl(`/articles`), {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
    });

    if (!response.ok) {
      return NextResponse.json(
          {error: 'FastAPIからのデータ取得に失敗しました'},
          {status: response.status}
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Backend fetch error:', error);
    return NextResponse.json(
        {error: 'Internal Server Error'},
        {status: 500}
    );
  }
}