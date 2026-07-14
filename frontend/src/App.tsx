'use client';

import {useEffect, useState} from 'react';

type Article = {
  id: number;
  title: string;
  content: string;
};

export default function App() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // ログアウトボタンを押したときの処理
  const handleLogout = async () => {
    try {
      const response = await fetch('/api/logout', {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('ログアウト処理に失敗しました');
      }

      // クッキーが消去された状態でログイン画面へ強制遷移
      window.location.href = '/login';
    } catch (err) {
      alert(err instanceof Error ? err.message : '不明なエラーが発生しました');
    }
  };

  useEffect(() => {
    const controller = new AbortController();

    const loadArticles = async () => {
      try {
        const response = await fetch('/api/articles', {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error('APIエラーが発生しました');
        }

        const data: Article[] = await response.json();
        setArticles(data);
      } catch (err) {
        if (controller.signal.aborted) {
          return;
        }
        setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    };

    void loadArticles();

    return () => controller.abort();
  }, []);

  return (
      <main className="page-shell">
        {/* カードデザインの内側にボタンを組み込むための position: 'relative' を追加 */}
        <section className="card" style={{position: 'relative'}}>

          {/* 【位置調整】カードの右上に絶対配置(absolute)で綺麗に収めています */}
          <div style={{position: 'absolute', top: '1.5rem', right: '1.5rem'}}>
            <button
                onClick={handleLogout}
                style={{
                  padding: '0.4rem 0.8rem',
                  backgroundColor: '#ff4d4f',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  fontSize: '0.8rem',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                  transition: 'opacity 0.2s'
                }}
                onMouseEnter={(e) => (e.currentTarget.style.opacity = '0.8')}
                onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
            >
              ログアウト
            </button>
          </div>

          <p className="eyebrow">Next.js + FastAPI</p>
          <h1>バックエンド接続確認</h1>
          <p className="description">
            Next.jsの <code>route.ts</code> を経由して FastAPI の <code>/articles</code> を安全に取得します。
          </p>

          {loading && <p className="status">読み込み中...</p>}
          {error && <p className="error">エラー: {error}</p>}

          {!loading && !error && (
              <div className="table-wrap">
                <table>
                  <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Content</th>
                  </tr>
                  </thead>
                  <tbody>
                  {articles.map((article) => (
                      <tr key={article.id}>
                        <td>{article.id}</td>
                        <td>{article.title}</td>
                        <td>{article.content}</td>
                      </tr>
                  ))}
                  {articles.length === 0 && (
                      <tr>
                        <td colSpan={3}>記事がありません。</td>
                      </tr>
                  )}
                  </tbody>
                </table>
              </div>
          )}
        </section>
      </main>
  );
}
