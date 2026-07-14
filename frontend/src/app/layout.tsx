import type {Metadata} from 'next';
import type {ReactNode} from 'react';
import './globals.css';

export const metadata: Metadata = {
  title: 'Fast API Tutorial',
  description: 'FastAPI の /articles を表示する Next.js アプリ',
};

export default function RootLayout({children}: { children: ReactNode }) {
  return (
      <html lang="ja">
      <body>{children}</body>
      </html>
  );
}

