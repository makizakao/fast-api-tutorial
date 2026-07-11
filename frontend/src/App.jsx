import React, { useEffect, useState } from 'react';

const FRONTEND_PORT = 3000;
const BACKEND_PORT = 8000;

function App() {
    const [articles, setArticles] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        // FastAPIのAPIを叩く
        fetch(`${import.meta.env.VITE_API_URL}/articles`)
            .then((res) => {
                if (!res.ok) throw new Error('APIエラーが発生しました');
                return res.json();
            })
            .then((data) => setArticles(data))
            .catch((err) => setError(err.message));
    }, []);

    return (
        <div style={{ padding: '20px' }}>
            <h1>バックエンド接続確認</h1>
            {error && <p style={{ color: 'red' }}>エラー: {error}</p>}
            <table border="1" style={{ borderCollapse: 'collapse', width: '100%' }}>
                <thead>
                <tr>
                    <th style={{ padding: '10px' }}>ID</th>
                    <th style={{ padding: '10px' }}>Title</th>
                    <th style={{ padding: '10px' }}>Content</th>
                </tr>
                </thead>
                <tbody>
                {articles.map((article) => (
                    <tr key={article.id}>
                        <td style={{ padding: '10px' }}>{article.id}</td>
                        <td style={{ padding: '10px' }}>{article.title}</td>
                        <td style={{ padding: '10px' }}>{article.content}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default App;