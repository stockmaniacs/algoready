import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'AlgoReady - Your Brokers. Your Strategies. One Trading Workspace.',
  description: 'Connect your broker accounts, apply pre-built trading strategies, and execute trades directly on your charts.',
  keywords: 'trading, algo trading, broker integration, strategy, signals',
};

export const viewport = {
  themeColor: '#0f172a',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} font-sans antialiased bg-background-dark text-neutral-100 min-h-screen`}>
        {children}
      </body>
    </html>
  );
}