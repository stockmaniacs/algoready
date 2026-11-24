/** @type {import('next').NextConfig} */
const nextConfig = {
  // Production settings for Cloudflare Pages
  output: 'export',
  compress: true,
  
  // Image optimization
  images: {
    domains: ['localhost', 'algoready.pages.dev'],
    unoptimized: true,
  },
  
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://api.algoready.dev',
    NEXT_PUBLIC_WS_URL: process.env.NEXT_PUBLIC_WS_URL || 'wss://api.algoready.dev',
  },
  
  // React strict mode
  reactStrictMode: true,
  
  // ESLint
  eslint: {
    ignoreDuringBuilds: true,
  },
  
  // TypeScript
  typescript: {
    ignoreBuildErrors: true,
  },
};

module.exports = nextConfig;