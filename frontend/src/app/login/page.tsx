'use client';

import React, {useState} from 'react';
import {useRouter} from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(false);

    if (!username || !password) {
      setError('ユーザー名とパスワードを入力してください');
      return;
    }

    setLoading(true);

    try {
      // 自サーバーの route.ts (/api/login) を叩く
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password}),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'ログインに失敗しました');
      }

      // ログイン成功後の遷移先（例: トップページやダッシュボード）
      router.push('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : '予期せぬエラーが発生しました');
    } finally {
      setLoading(false);
    }
  };

  return (
      <main style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh'}}>
        <div style={{padding: '2rem', border: '1px solid #ccc', borderRadius: '8px', width: '320px'}}>
          <h2 style={{marginBottom: '1.5rem', textAlign: 'center'}}>ログイン</h2>

          <form onSubmit={handleSubmit}>
            <div style={{marginBottom: '1rem'}}>
              <label style={{display: 'block', marginBottom: '0.5rem'}}>ユーザー名:</label>
              <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc'}}
                  disabled={loading}
              />
            </div>

            <div style={{marginBottom: '1.5rem'}}>
              <label style={{display: 'block', marginBottom: '0.5rem'}}>パスワード:</label>
              <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{width: '100%', padding: '0.5rem', borderRadius: '4px', border: '1px solid #ccc'}}
                  disabled={loading}
              />
            </div>

            {error && (
                <p style={{color: 'red', fontSize: '0.875rem', marginBottom: '1rem'}}>{error}</p>
            )}

            <button
                type="submit"
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: loading ? '#ccc' : '#0070f3',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: loading ? 'not-allowed' : 'pointer',
                }}
                disabled={loading}
            >
              {loading ? '処理中...' : 'ログイン'}
            </button>
          </form>
        </div>
      </main>
  );
}
