import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig(({ command }) => ({
  plugins: [react()],
  base: command === 'build' ? '/ntl-running-tournaments/html/' : '/',
  build: {
    outDir: '../html',
    emptyOutDir: true,
  },
  server: {
    fs: {
      allow: [
        // Allow serving files from one level up to the project root
        '..'
      ]
    }
  }
}))
