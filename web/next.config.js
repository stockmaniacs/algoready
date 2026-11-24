/** @type {import('next').NextConfig} */
const nextConfig = {
  // Production settings for Cloudflare Pages
  output: 'standalone',
  compress: true,
  
  // Image optimization
  images: {
    domains: ['localhost', 'algoready.pages.dev'],
  },
  
  // Environment variables
  env: {
    API_URL: process.env.API_URL || 'https://api.algoready.dev',
  },
  
  // Disable image optimization in production for better build times
  experimental: {
    optimizeCss: false,
  },
  
  // React strict mode
  reactStrictMode: true,
  
  // SWSW target for browsers
  target: 'serverless',
};

module.exports = nextConfig;