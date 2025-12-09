import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Local development config (no base path)
export default defineConfig({
  plugins: [react()],
  base: '/',
  server: {
    port: 3000
  }
})

