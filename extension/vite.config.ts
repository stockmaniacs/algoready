import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteStaticCopy } from 'vite-plugin-static-copy';
import path from 'path';

export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        {
          src: 'manifest.json',
          dest: '.',
        },
        {
          src: 'public/icons',
          dest: 'public',
        },
        {
          src: 'public/styles.css',
          dest: 'public',
        },
        {
          src: 'public/overlay.css',
          dest: 'public',
        },
        {
          src: 'public/overlay.js',
          dest: 'public',
        },
      ],
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: false,
    minify: 'esbuild',
    rollupOptions: {
      input: {
        popup: 'src/popup.html',
        sidepanel: 'src/sidepanel.html',
        options: 'src/options.html',
        background: 'src/background.js',
        content: 'src/content.js',
      },
      output: {
        entryFileNames: (chunkInfo) => {
          if (chunkInfo.name === 'background') {
            return 'background.js';
          }
          return 'assets/[name].js';
        },
        chunkFileNames: 'assets/[name].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name === 'styles.css') {
            return 'public/styles.css';
          }
          if (assetInfo.name === 'overlay.css') {
            return 'public/overlay.css';
          }
          if (assetInfo.name === 'overlay.js') {
            return 'public/overlay.js';
          }
          return 'assets/[name].[ext]';
        },
      },
    },
  },
  define: {
    'process.env': {},
  },
});