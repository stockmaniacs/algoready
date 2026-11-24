import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import fs from 'fs';

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'copy-html-files',
      writeBundle() {
        const distDir = path.resolve(__dirname, 'dist');
        
        // Copy HTML files from src to dist root
        const htmlFiles = ['popup.html', 'options.html', 'sidepanel.html'];
        htmlFiles.forEach(file => {
          const src = path.join(__dirname, 'src', file);
          const dest = path.join(distDir, file);
          if (fs.existsSync(src)) {
            fs.copyFileSync(src, dest);
          }
        });
        
        // Copy manifest
        fs.copyFileSync(
          path.resolve(__dirname, 'manifest.json'),
          path.join(distDir, 'manifest.json')
        );
        
        // Copy icons
        const iconsDir = path.join(distDir, 'public', 'icons');
        fs.mkdirSync(iconsDir, { recursive: true });
        ['icon-16.png', 'icon-32.png', 'icon-48.png', 'icon-128.png'].forEach(icon => {
          const src = path.join(__dirname, 'public', 'icons', icon);
          const dest = path.join(iconsDir, icon);
          if (fs.existsSync(src)) {
            fs.copyFileSync(src, dest);
          }
        });
        
        // Copy overlay files to dist root
        ['overlay.css', 'overlay.js'].forEach(file => {
          const src = path.join(__dirname, 'public', file);
          const dest = path.join(distDir, file);
          if (fs.existsSync(src)) {
            fs.copyFileSync(src, dest);
          }
        });
        
        // Remove empty assets folder that vite creates
        const assetsDir = path.join(distDir, 'assets');
        if (fs.existsSync(assetsDir) && fs.readdirSync(assetsDir).length === 0) {
          fs.rmdirSync(assetsDir);
        }
        
        // Remove src folder from dist (it's not needed)
        const srcDistDir = path.join(distDir, 'src');
        if (fs.existsSync(srcDistDir)) {
          fs.rmSync(srcDistDir, { recursive: true, force: true });
        }
      }
    }
  ],
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
          if (chunkInfo.name === 'content') {
            return 'content.js';
          }
          if (chunkInfo.name === 'options') {
            return 'options.js';
          }
          if (chunkInfo.name === 'sidepanel') {
            return 'sidepanel.js';
          }
          return '[name].js';
        },
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]',
      },
    },
  },
  define: {
    'process.env': {},
  },
});
