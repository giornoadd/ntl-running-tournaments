import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/ntl-running-tournaments/html/',
  build: {
    outDir: '../html',
    emptyOutDir: false, // We don't want to nuke the entire folder since data.js lives there, BUT we might need to be careful here...
    // Actually, data.js is generated via python so we CAN empty outDir except no we can't because it's static HTML folder. 
    // Wait, the best approach is to configure emptyOutDir: false so it just overwrites index.html and assets/
  },
  server: {
    fs: {
      allow: [
        // Allow serving files from one level up to the project root
        '..'
      ]
    }
  }
})
